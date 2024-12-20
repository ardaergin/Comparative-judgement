from psychopy import visual, core, event
import os
from app.id_prompt import get_participant_id
from app.stimuli import load_stimuli, setup_stimuli
from app.data_handler import setup_data_file
from app.trial_similarity import run_similarity_trials, run_practice
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
    size=(1024, 768),
    fullscr=True,
    color=[1, 1, 1],
    units='pix'
)

# ======================
# Experiment Information
# ======================
experiment_info = visual.TextStim(
    win,
    text="Welcome to the experiment!\n\nIn this study, you will be comparing images to assess their similarity to a reference image. "
         "The results of this study will help us better understand how humans make visual judgments.\n\n"
         "Press SPACE to continue.",
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
experiment_info.draw()
win.flip()
event.waitKeys(keyList=['space'])

# ======================
# Informed Consent
# ======================
consent_message = visual.TextStim(
    win,
    text="Informed Consent\n\nBy participating in this experiment, you agree that your responses will be anonymized and used for research purposes. "
         "You may withdraw from the study at any time by pressing ESCAPE.\n\nIf you agree to participate, press SPACE to continue.",
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
consent_message.draw()
win.flip()
consent_key = event.waitKeys(keyList=['space', 'escape'])

if 'escape' in consent_key:
    win.close()
    core.quit()

# ======================
# Participant ID
# ======================
participant_id = get_participant_id(win)

# ======================
# Data Handling
# ======================
data_file, writer = setup_data_file(participant_id)

# ======================
# Stimuli Setup
# ======================
# Practice stimuli
practice_comparison_files = load_stimuli('images_practice/comparison')
practice_trial_list = setup_stimuli(practice_comparison_files, 1)  # 1 repeat for practice

# Main stimuli
comparison_files = load_stimuli('images/comparison')
trial_list = setup_stimuli(comparison_files, pair_repeats)

# ======================
# Instructions Screen
# ======================
instructions = visual.TextStim(
    win, 
    text="On each trial, you will see a reference image at the top and two images below. "
         "You will make judgements on SIMILARITY."
         "\n\nPress the LEFT arrow if the left image is more similar to the reference, or "
         "RIGHT arrow if the right image is more similar. "
         f"\n\n\Please keep in mind that you have {skip_time_limit} seconds to press a key for your response. "
         "Therefore, you must be fast. "
         "\n\nPress SPACE to begin.",
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
instructions.draw()
win.flip()
event.waitKeys(keyList=['space'])

# ======================
# Practice Round
# ======================
practice_message = visual.TextStim(
    win,
    text="We will now have a practice round. "
    "Use this time to familiarize yourself with the task."
    "\n\nPress SPACE to begin.",
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
practice_message.draw()
win.flip()
event.waitKeys(keyList=['space'])

run_practice(win, practice_trial_list, skip_time_limit)


# ======================
# Main Trial Loop: Similarity
# ======================
similarity_message = visual.TextStim(
    win,
    text="Now you will have the real trials to judge similarity. "
    "\n\nPress SPACE to begin.",
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
similarity_message.draw()
win.flip()
event.waitKeys(keyList=['space'])

run_similarity_trials(win, trial_list, writer, skip_time_limit, adaptive_mode)

# ======================
# Main Trial Loop: Liking
# ======================
liking_message = visual.TextStim(
    win,
    text="Now you will have a second round of trials where you will choose which image you like more. "
    "\n\nPress SPACE to begin.",
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
liking_message.draw()
win.flip()
event.waitKeys(keyList=['space'])

run_liking_trials(win, trial_list, participant_id, skip_time_limit)

# ======================
# Demographic Questions
# ======================
liking_message = visual.TextStim(
    win,
    text="Finally, we would like you to answer some basic questions about yourself. "
    "\n\nPress SPACE to continue.",
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
liking_message.draw()
win.flip()
event.waitKeys(keyList=['space'])

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
