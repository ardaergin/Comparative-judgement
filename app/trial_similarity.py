from psychopy import visual, core, event
import os
from app.adaptive_algorithm import ACJ

def run_trials(
    win, 
    trial_list, 
    writer=None, 
    skip_time_limit=4, 
    prompt_text="Which is more similar to the reference image?\n(left = D, right = K)", 
    image_folder="images/trials/comparison", 
    reference_image_path=None, 
    adaptive_mode=False
):
    """
    General function to run trials.

    Parameters:
        win: PsychoPy Window object.
        trial_list: List of trials (pairs of images).
        writer: CSV writer object for saving responses (optional).
        skip_time_limit: Time in seconds before a trial is skipped.
        prompt_text: Prompt text to display above the images.
        image_folder: Path to the folder containing comparison images.
        reference_image_path: Path to the reference image (optional).
        adaptive_mode: Boolean for adaptive judgment mode.
    """
    # Create reference image stimulus if provided
    reference_stim = None
    if reference_image_path:
        reference_stim = visual.ImageStim(win, image=reference_image_path, size=(300, 300), pos=(0, 150))
    
    fixation = visual.TextStim(win, text="+", height=50, color='black', pos=(0, 0))  # Center fixation

    missed_message = visual.TextStim(
        win,
        text="You missed the last trial.\nPlease respond faster.\n\nRemember we are interested in your initial impressions.",
        color='black',
        height=24,
        wrapWidth=800,
        pos=(0, 0)
    )

    clock = core.Clock()

    # Initialize adaptive judgment system if needed
    acj = ACJ([item for pair in trial_list for item in pair]) if adaptive_mode else None

    for trial_num in range(1, len(trial_list) + 1):
        # Select pair
        if adaptive_mode:
            left_image_name, right_image_name = acj.select_pair()
        else:
            left_image_name, right_image_name = trial_list[trial_num - 1]

        # Show fixation point
        fixation.draw()
        win.flip()
        core.wait(1)

        # Create image stimuli
        left_stim = visual.ImageStim(win, image=os.path.join(image_folder, left_image_name), size=(300, 300), pos=(-250, -150))
        right_stim = visual.ImageStim(win, image=os.path.join(image_folder, right_image_name), size=(300, 300), pos=(250, -150))

        # Create prompt above the images
        prompt = visual.TextStim(
            win,
            text=prompt_text,
            color='black',
            height=24,
            pos=(0, 350)
        )

        # Draw stimuli
        prompt.draw()
        if reference_stim:
            reference_stim.draw()
        left_stim.draw()
        right_stim.draw()
        win.flip()

        # Collect response
        clock.reset()
        keys = event.waitKeys(keyList=['d', 'k', 'escape'], timeStamped=clock, maxWait=skip_time_limit)

        if keys:
            key, rt = keys[0]
            if key == 'escape':
                break  # Allow experimenter to quit
            else:
                winner = left_image_name if key == 'd' else right_image_name

                if writer:  # Only write to file if writer is provided
                    writer.writerow([trial_num, left_image_name, right_image_name, key, rt])

                # Highlight chosen image as feedback
                if key == 'd':
                    left_stim.color = [0.5, 0.5, 0.5]  # Dim the left image
                elif key == 'k':
                    right_stim.color = [0.5, 0.5, 0.5]  # Dim the right image

                # Draw feedback
                prompt.draw()
                if reference_stim:
                    reference_stim.draw()
                left_stim.draw()
                right_stim.draw()
                win.flip()
                core.wait(0.5)  # Show feedback for 0.5 seconds

                if adaptive_mode:
                    acj.record_comparison(left_image_name, right_image_name, winner)
                    acj.update_parameters()
        else:
            # Trial was skipped
            missed_message.draw()
            win.flip()
            core.wait(2)  # Show missed message for 2 seconds
            if writer:
                writer.writerow([trial_num, left_image_name, right_image_name, "missing", "N/A"])
            continue
