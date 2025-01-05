from psychopy import visual, core, event
import os
from app.id_prompt import get_participant_id
from app.stimuli import load_stimuli, setup_stimuli
from app.data_handler import setup_data_file
from app.trial_similarity import run_trials
from app.trials_liking import run_liking_trials
from app.demographics import collect_demographics

# ======================
# Parameters
# ======================
pair_repeats = 1
skip_time_limit = 4
adaptive_mode = False
practice_rounds = 3

# Set up PsychoPy window
win = visual.Window(
    fullscr=True,
    color=[1, 1, 1],
    units='pix'
)

# ======================
# Experiment Information
# ======================
with open("texts/0_experiment_info.txt", "r") as file:
    experiment_info_text = file.read()

experiment_info = visual.TextStim(
    win,
    text=experiment_info_text,
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
experiment_info.draw()
win.flip()
event.waitKeys(keyList=['space'])

# ======================
# Informed Consent
# ======================
with open("texts/1_informed_consent.txt", "r") as file:
    informed_consent_text = file.read()

informed_consent = visual.TextStim(
    win,
    text=informed_consent_text,
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
informed_consent.draw()
win.flip()
consent_key = event.waitKeys(keyList=['space', 'escape'])

if 'escape' in consent_key:
    win.close()
    core.quit()

# ======================
# Participant ID
# ======================
with open("texts/2_participant_id.txt", "r") as file:
    participant_id_text = file.read()

participant_id = get_participant_id(win, participant_id_text)

# ======================
# Data Handling
# ======================
data_file, writer = setup_data_file(participant_id)

# ======================
# Stimuli Setup
# ======================
# Practice stimuli
practice_comparison_files = load_stimuli('images/practice/comparison')
practice_trial_list = setup_stimuli(practice_comparison_files, 1)  # 1 repeat for practice

# Main stimuli
comparison_files = load_stimuli('images/trials/comparison')
trial_list = setup_stimuli(comparison_files, pair_repeats)

# ======================
# Pre-instructions Screen
# ======================
with open("texts/3_pre_instructions.txt", "r") as file:
    pre_instructions_text = file.read()

pre_instructions = visual.TextStim(
    win,
    text=pre_instructions_text,
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
pre_instructions.draw()
win.flip()
event.waitKeys(keyList=['space'])

# ======================
# Instructions: Practice Rounds
# ======================
with open("texts/4_practice_instructions.txt", "r") as file:
    practice_instructions_text = file.read()

practice_instructions = visual.TextStim(
    win,
    text=practice_instructions_text,
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
practice_instructions.draw()
win.flip()
event.waitKeys(keyList=['space'])

# ======================
# Practice Rounds
# ======================
run_trials(
    win, 
    trial_list=practice_trial_list, 
    prompt_text="Which product on the bottom is more similar to the product on top?\n(left = D, right = K)",
    image_folder="images/practice/comparison", 
    reference_image_path="images/practice/reference/ref_image.jpg", 
    skip_time_limit=skip_time_limit
)

# ======================
# Instructions: Similarity Trials
# ======================
with open("texts/5_trial_instructions_sim.txt", "r") as file:
    trial_instructions_sim_text = file.read()

trial_instructions_sim = visual.TextStim(
    win,
    text=trial_instructions_sim_text,
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
trial_instructions_sim.draw()
win.flip()
event.waitKeys(keyList=['space'])

# ======================
# Main Trial Loop: Similarity
# ======================
run_trials(
    win, 
    trial_list=trial_list, 
    writer=writer, 
    prompt_text="Which plant-based steak is more similar to the beef steak?\n(left = D, right = K)?",
    image_folder="images/trials/comparison", 
    reference_image_path="images/trials/reference/ref_image.png", 
    skip_time_limit=skip_time_limit, 
    adaptive_mode=adaptive_mode
)

# ======================
# Instructions: Liking Trials
# ======================
with open("texts/6_trial_instructions_liking.txt", "r") as file:
    trial_instructions_liking_text = file.read()

trial_instructions_liking = visual.TextStim(
    win,
    text=trial_instructions_liking_text,
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)

trial_instructions_liking.draw()
win.flip()
event.waitKeys(keyList=['space'])

# ======================
# Main Trial Loop: Liking
# ======================
# run_liking_trials(win, trial_list, participant_id, skip_time_limit)
run_trials(
    win, 
    trial_list=trial_list, 
    writer=writer, 
    prompt_text="Which of the two plant-based steak do you like most?\n(left = D, right = K)?",
    image_folder="images/trials/comparison", 
    reference_image_path=None,  # No reference image for liking trials
    skip_time_limit=skip_time_limit
)

# ======================
# Pre-demographics
# ======================
with open("texts/7_pre_demographics.txt", "r") as file:
    pre_demographics_text = file.read()

pre_demographics = visual.TextStim(
    win,
    text=pre_demographics_text,
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)

pre_demographics.draw()
win.flip()
event.waitKeys(keyList=['space'])

# ======================
# Demographic Questions
# ======================
collect_demographics(win, participant_id)

# ======================
# End of Experiment
# ======================
thankyou = visual.TextStim(win, text="Thank you for participating!", height=24, color='black')
thankyou.draw()
win.flip()
core.wait(2)

# Cleanup
data_file.close()
win.close()
core.quit()
