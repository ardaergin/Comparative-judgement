from psychopy import visual, event, core
import os, random, csv
import itertools

# ======================
# Parameters
# ======================
pair_repeats = 2  # How many times to show each pair of images
skip_time_limit = 3  # Time in seconds to skip a trial if no response is made

# ======================
# Set up PsychoPy Window
# ======================
win = visual.Window(
    size=(1024, 768),
    fullscr=True,  # Enable fullscreen
    color=[1, 1, 1],  # Set background to white
    units='pix'
)

# ======================
# Ask for Participant ID
# ======================
id_prompt = visual.TextStim(win, 
    text="Please enter your Participant ID:\n\n(Type your ID and press ENTER to continue)", 
    color='black', height=32, wrapWidth=800, pos=(0, 50))
id_display = visual.TextStim(win, text="", color='black', height=32, pos=(0, -50))

participant_id = ""  # Initialize empty ID string
while True:
    id_prompt.draw()
    id_display.setText(participant_id)  # Update the display with the current input
    id_display.draw()
    win.flip()
    
    keys = event.waitKeys()  # Wait for key input
    for key in keys:
        if key == 'return':  # Enter key to submit
            if len(participant_id) > 0:  # Ensure the ID is not empty
                break
        elif key == 'backspace':  # Remove the last character
            participant_id = participant_id[:-1]
        elif key in ['escape']:  # Allow experimenter to quit
            win.close()
            core.quit()
        else:
            # Add character to the participant ID
            participant_id += key
    
    # Break the loop if the Enter key was pressed with a valid ID
    if 'return' in keys and len(participant_id) > 0:
        break

# Create data directory if it doesn't exist
if not os.path.isdir('data'):
    os.makedirs('data')

dataFileName = os.path.join('data', f"{participant_id}.csv")

# ======================
# Load images
# ======================
reference_image_path = 'images/reference/ref_image.png'
comparison_dir = 'images/comparison'

# Get all comparison images
comparison_files = [f for f in os.listdir(comparison_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Make sure we have at least two images
if len(comparison_files) < 2:
    raise ValueError("Not enough comparison images found. At least two are required.")

# ======================
# Generate all unique pairs
# ======================
all_pairs = list(itertools.combinations(comparison_files, 2))
trial_list = all_pairs * pair_repeats
random.shuffle(trial_list)

# ======================
# Create stimuli
# ======================
reference_stim = visual.ImageStim(win, image=reference_image_path, size=(300, 300), pos=(0, 200))
fixation = visual.TextStim(win, text="+", height=50, color='black')  # Fixation cross

# ======================
# Data handling
# ======================
if os.path.exists(dataFileName):
    baseName, fileExt = os.path.splitext(dataFileName)
    count = 1
    while os.path.exists(dataFileName):
        dataFileName = f"{baseName}_{count}{fileExt}"
        count += 1

data_file = open(dataFileName, 'w', newline='')
writer = csv.writer(data_file)
writer.writerow(['trial', 'left_image', 'right_image', 'response', 'rt'])

# ======================
# Instruction Screen
# ======================
instructions = visual.TextStim(
    win, 
    text="On each trial, you will see a reference image at the top and two images below. Press the LEFT arrow if the left image is more similar to the reference, or RIGHT arrow if the right image is more similar. Press any key to begin.",
    height=24, wrapWidth=800, color='black', pos=(0, 0)
)
instructions.draw()
win.flip()
event.waitKeys()  # Wait for any key to start

# ======================
# Main Trial Loop
# ======================
clock = core.Clock()
for trial_num, (left_image_name, right_image_name) in enumerate(trial_list, start=1):
    fixation.draw()
    win.flip()
    core.wait(1)  # Display fixation for 1 second
    
    left_stim = visual.ImageStim(win, image=os.path.join(comparison_dir, left_image_name), size=(300, 300), pos=(-200, -100))
    right_stim = visual.ImageStim(win, image=os.path.join(comparison_dir, right_image_name), size=(300, 300), pos=(200, -100))
    
    reference_stim.draw()
    left_stim.draw()
    right_stim.draw()
    
    prompt = visual.TextStim(
        win, 
        text="Which is more similar to the reference image?\nLeft (←) or Right (→)", 
        color='black', height=24, pos=(0, -300)
    )
    prompt.draw()
    win.flip()
    
    clock.reset()
    keys = event.waitKeys(keyList=['left', 'right', 'escape'], timeStamped=clock, maxWait=skip_time_limit)
    
    if keys:
        key, rt = keys[0]
        if key == 'escape':
            break
        else:
            writer.writerow([trial_num, left_image_name, right_image_name, key, rt])
    else:
        writer.writerow([trial_num, left_image_name, right_image_name, "missing", "N/A"])
        continue

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
