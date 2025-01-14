from psychopy import visual, core, event
import os
from app.adaptive_algorithm import ACJ
import random

def run_trials(
    win, 
    trial_list, 
    writer=None, 
    skip_time_limit=4, 
    prompt_text="Which is more similar to the reference image?\n(left = D, right = K)", 
    image_folder="images/trials/comparison", 
    comparison_images=None,  # Preloaded comparison images
    reference_image=None,    # Preloaded reference image
    adaptive_mode=False,
    round_type="unknown"
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
        comparison_images: Dictionary of preloaded comparison ImageStim objects.
        reference_image: Preloaded reference ImageStim object.
        adaptive_mode: Boolean for adaptive judgment mode.
        round_type: String specifying the type of the round (e.g., "practice", "similarity", "liking").
    """
    # Use preloaded reference image
    reference_stim = reference_image

    # Fixation stimulus
    fixation = visual.TextStim(win, text="+", height=50, color='black', pos=(0, 0))

    # Missed trial message
    missed_message = visual.TextStim(
        win,
        text="You missed the last trial.\nPlease respond faster.\n\nRemember we are interested in your initial impressions.\n\nPress the SPACE BAR to continue.",
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

        # Randomize the order of the images
        if random.choice([True, False]):  # 50% chance to swap
            left_image_name, right_image_name = right_image_name, left_image_name

        # Show fixation point
        fixation.draw()
        win.flip()
        core.wait(0.5)

        # Use preloaded comparison images
        left_stim = comparison_images[left_image_name]
        right_stim = comparison_images[right_image_name]

        # Update their positions for the trial
        left_stim.pos = (-250, -150)
        right_stim.pos = (250, -150)

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
                    writer.writerow([trial_num, round_type, left_image_name, right_image_name, key, rt])

                # Highlight chosen image with a red border
                chosen_stim = left_stim if key == 'd' else right_stim
                red_border = visual.Rect(
                    win,
                    width=chosen_stim.size[0] + 10,
                    height=chosen_stim.size[1] + 10,
                    lineColor='red',
                    lineWidth=5,
                    pos=chosen_stim.pos
                )

                # Draw feedback
                prompt.draw()
                if reference_stim:
                    reference_stim.draw()
                left_stim.draw()
                right_stim.draw()
                red_border.draw()  # Draw the red border
                win.flip()
                core.wait(0.5)  # Show feedback for 0.5 seconds

                if adaptive_mode:
                    acj.record_comparison(left_image_name, right_image_name, winner)
                    acj.update_parameters()
        else:
            # Trial was skipped
            missed_message.draw()
            win.flip()
            # Wait for space bar to continue
            event.waitKeys(keyList=['space'])
            if writer:
                writer.writerow([trial_num, round_type, left_image_name, right_image_name, "missing", "N/A"])
            continue
