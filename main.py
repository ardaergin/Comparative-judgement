from psychopy import visual, core
import os
from app.id_prompt import get_participant_id
from app.stimuli import load_stimuli, setup_stimuli
from app.data_handler import setup_data_file
from app.trial import run_trials

# ======================
# Parameters
# ======================
pair_repeats = 2
skip_time_limit = 3

# Set up PsychoPy window
win = visual.Window(
    size=(1024, 768),
    fullscr=True,
    color=[1, 1, 1],
    units='pix'
)

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
comparison_files = load_stimuli('images/comparison')
trial_list = setup_stimuli(comparison_files, pair_repeats)

# ======================
# Instructions Screen
# ======================
instructions = visual.TextStim(
    win, 
    text="On each trial, you will see a reference image at the top and two images below. "
         "Press the LEFT arrow if the left image is more similar to the reference, or "
         "RIGHT arrow if the right image is more similar. Press any key to begin.",
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
instructions.draw()
win.flip()
core.wait(2)

# ======================
# Main Trial Loop
# ======================
run_trials(win, trial_list, writer, skip_time_limit)

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
