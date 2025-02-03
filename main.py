from psychopy import visual, core, event
import os
from app.id_prompt import get_participant_id
from app.stimuli import load_stimuli, setup_stimuli, preload_images
from app.data_handler import setup_data_file
from app.trials import run_trials
from app.demographics import collect_demographics
from app.instruction_images import create_scaled_image
from app.feedback import *

# ======================
# Parameters
# ======================

## Experiment parameters
pair_repeats = 1
skip_time_limit = 4

## Visual parameters
experiment_font = "Times New Roman"

## Set up PsychoPy window
win = visual.Window(
    fullscr=True,
    # size=(1280, 720),
    color=[1, 1, 1],
    units='pix'
)


# ======================
# Stimuli Setup and Preloading
# ======================
# Practice stimuli
practice_comparison_files = load_stimuli('images/practice/comparison')  # Load image filenames
practice_preloaded_images = preload_images(win, 'images/practice/comparison', practice_comparison_files)  # Preload images
practice_trial_list = setup_stimuli(practice_comparison_files, 1)  # Generate trial list (1 repeat for practice)
practice_reference_image = visual.ImageStim(win, image="images/practice/reference/ref_image.png", size=(300, 300), pos=(0, 100))  # Preload reference image

# Main stimuli
comparison_files = load_stimuli('images/trials/comparison')  # Load image filenames
trial_preloaded_images = preload_images(win, 'images/trials/comparison', comparison_files)  # Preload images
trial_list = setup_stimuli(comparison_files, pair_repeats)  # Generate trial list
main_reference_image = visual.ImageStim(win, image="images/trials/reference/ref_image.png", size=(300, 300), pos=(0, 100))  # Preload reference image


# ======================
# Experiment Information
# ======================

# with open("texts/0_experiment_info.txt", "r") as file:
#     experiment_info_text = file.read()
# experiment_info = visual.TextStim(
#     win,
#     text=experiment_info_text,
#     height=24, wrapWidth=800, color='black', pos=(0, 0)
# )

experiment_info = create_scaled_image(win, "texts/0_experiment_info.png")
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
    height=24, wrapWidth=800, color='black', pos=(0, 0),
    font=experiment_font,
    alignText='left', anchorHoriz='center'
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

participant_id = get_participant_id(win, participant_id_text, experiment_font)


# ======================
# Data Handling
# ======================
data_file, writer = setup_data_file(participant_id)


# ======================
# Pre-instructions Screen
# ======================
with open("texts/3_pre_instructions.txt", "r") as file:
    pre_instructions_text = file.read()

pre_instructions = visual.TextStim(
    win,
    text=pre_instructions_text,
    height=24, wrapWidth=800, color='black', pos=(0, 0),
    font=experiment_font,
    alignText='left', anchorHoriz='center'
)
pre_instructions.draw()
win.flip()
event.waitKeys(keyList=['space'])


# ======================
# Instructions: Practice Rounds
# ======================

# with open("texts/4_practice_instructions.txt", "r") as file:
#     practice_instructions_text = file.read()
# practice_instructions = visual.TextStim(
#     win,
#     text=practice_instructions_text,
#     height=24, wrapWidth=800, color='black', pos=(0, 0)
# )

practice_instructions = create_scaled_image(win, "texts/4_practice_instructions.png")
practice_instructions.draw()
win.flip()
event.waitKeys(keyList=['space'])

# practice_instructions = create_scaled_image(win, "texts/4_practice_instructions_visual.png")
# practice_instructions.draw()
# win.flip()
# event.waitKeys(keyList=['space'])

# ======================
# Practice Rounds
# ======================
run_trials(
    win, 
    trial_list=practice_trial_list, 
    writer=writer, 
    prompt_text="Which of the products on the bottom is more similar to the product on top?\n(left = D, right = K)",
    comparison_images=practice_preloaded_images,
    reference_image=practice_reference_image,
    skip_time_limit=skip_time_limit, 
    round_type="practice",
    num_breaks=0,
    left_text="Citrus fruit A",
    right_text="Citrus fruit B",
    reference_text="Orange"
)

# Aftermath of the Practice rounds:
with open("texts/4_practice_aftermath.txt", "r") as file:
    practice_aftermath_text = file.read()

practice_aftermath = visual.TextStim(
    win,
    text=practice_aftermath_text,
    height=24, wrapWidth=800, color='black', pos=(0, 0),
    font=experiment_font,
    alignText='left', anchorHoriz='center'
)
practice_aftermath.draw()
win.flip()
event.waitKeys(keyList=['space'])

# ======================
# Instructions: Similarity Trials
# ======================

# with open("texts/5_trial_instructions_sim.txt", "r") as file:
#     trial_instructions_sim_text = file.read()
# trial_instructions_sim = visual.TextStim(
#     win,
#     text=trial_instructions_sim_text,
#     height=24, wrapWidth=800, color='black', pos=(0, 0)
# )

trial_instructions_sim = create_scaled_image(win, "texts/5_trial_instructions_sim.png")
trial_instructions_sim.draw()
win.flip()
event.waitKeys(keyList=['space'])

# trial_instructions_sim = create_scaled_image(win, "texts/5_trial_instructions_sim_visual.png")
# trial_instructions_sim.draw()
# win.flip()
# event.waitKeys(keyList=['space'])


# ======================
# Main Trial Loop: Similarity
# ======================
run_trials(
    win, 
    trial_list=trial_list, 
    writer=writer, 
    prompt_text="Which of the two plant-based steaks on the bottom is more similar to the beef steak on top?\n(left = D, right = K)?",
    comparison_images=trial_preloaded_images,
    reference_image=main_reference_image,
    skip_time_limit=skip_time_limit, 
    round_type="similarity",
    num_breaks=3,
    break_wait_time=20,
    left_text="Plant-based Steak A",
    right_text="Plant-based Steak B",
    reference_text="Real Steak"
)


# ======================
# Instructions: Liking Trials
# ======================

# with open("texts/6_trial_instructions_liking.txt", "r") as file:
#     trial_instructions_liking_text = file.read()
# trial_instructions_liking = visual.TextStim(
#     win,
#     text=trial_instructions_liking_text,
#     height=24, wrapWidth=800, color='black', pos=(0, 0)
# )

trial_instructions_liking = create_scaled_image(win, "texts/6_trial_instructions_liking.png")
trial_instructions_liking.draw()
win.flip()
event.waitKeys(keyList=['space'])

# trial_instructions_liking = create_scaled_image(win, "texts/6_trial_instructions_liking_visual.png")
# trial_instructions_liking.draw()
# win.flip()
# event.waitKeys(keyList=['space'])

# ======================
# Main Trial Loop: Liking
# ======================
# run_liking_trials(win, trial_list, participant_id, skip_time_limit)
run_trials(
    win, 
    trial_list=trial_list, 
    writer=writer, 
    prompt_text="Which of the two plant-based steaks do you like more?\n(left = D, right = K)?",
    comparison_images=trial_preloaded_images,
    reference_image=None, # or main_reference_image
    skip_time_limit=skip_time_limit, 
    round_type="liking",
    num_breaks=3,
    break_wait_time=20,
    left_text="Plant-based Steak A",
    right_text="Plant-based Steak B",
    reference_text="Real Steak"
)


# ======================
# Pre-demographics
# ======================
with open("texts/7_pre_demographics.txt", "r") as file:
    pre_demographics_text = file.read()

pre_demographics = visual.TextStim(
    win,
    text=pre_demographics_text,
    height=24, wrapWidth=800, color='black', pos=(0, 0),
    font=experiment_font,
    alignText='left', anchorHoriz='center'
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
collect_feedback(win, participant_id)

# Show final message
show_final_message(win)

# Cleanup
data_file.close()
win.close()
core.quit()
