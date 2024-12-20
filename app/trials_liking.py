from psychopy import visual, event, core
import os

def run_liking_trials(win, trial_list, participant_id, skip_time_limit):
    """
    Runs a set of liking trials where participants select which image they like more.

    Parameters:
    - win: PsychoPy Window object
    - trial_list: List of image pairs for the trials
    - participant_id: Participant ID to name the output file
    - skip_time_limit: Time in seconds to wait for a response
    """
    # Prepare the output file
    output_file = f"data/{participant_id}_liking.csv"
    with open(output_file, 'w') as data_file:
        # Write header
        data_file.write("trial,left_image,right_image,response,rt\n")

        clock = core.Clock()
        fixation = visual.TextStim(win, text="+", height=50, color='black')  # Fixation cross

        for trial_num, (left_image_name, right_image_name) in enumerate(trial_list, start=1):
            # Show fixation point
            fixation.draw()
            win.flip()
            core.wait(1)  # Display fixation for 1 second

            # Create image stimuli
            left_stim = visual.ImageStim(win, image=os.path.join('images/comparison', left_image_name), size=(300, 300), pos=(-200, 0))
            right_stim = visual.ImageStim(win, image=os.path.join('images/comparison', right_image_name), size=(300, 300), pos=(200, 0))

            # Draw stimuli
            left_stim.draw()
            right_stim.draw()

            # Add a prompt
            prompt = visual.TextStim(
                win,
                text="Which image do you like more?\n\nPress LEFT (←) or RIGHT (→).",
                color='black',
                height=24,
                pos=(0, -250)
            )
            prompt.draw()
            win.flip()

            # Collect response
            clock.reset()
            keys = event.waitKeys(keyList=['left', 'right', 'escape'], timeStamped=clock, maxWait=skip_time_limit)

            if keys:
                key, rt = keys[0]
                if key == 'escape':
                    win.close()
                    core.quit()
                else:
                    # Save the response
                    response = 'left' if key == 'left' else 'right'
                    data_file.write(f"{trial_num},{left_image_name},{right_image_name},{response},{rt}\n")
            else:
                # No response within time limit
                data_file.write(f"{trial_num},{left_image_name},{right_image_name},missing,N/A\n")
                continue
