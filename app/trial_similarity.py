from psychopy import visual, core, event
import os
from app.adaptive_algorithm import ACJ


def run_practice(win, trial_list, skip_time_limit):
    reference_image_path = 'images/practice/reference/ref_image.jpg'
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

    for trial_num, (left_image_name, right_image_name) in enumerate(trial_list, start=1):
        # Show fixation point
        fixation.draw()
        win.flip()
        core.wait(1)

        # Create image stimuli
        left_stim = visual.ImageStim(win, image=os.path.join('images/practice/comparison', left_image_name), size=(300, 300), pos=(-200, -100))
        right_stim = visual.ImageStim(win, image=os.path.join('images/practice/comparison', right_image_name), size=(300, 300), pos=(200, -100))

        # Create prompt above the images
        prompt = visual.TextStim(
            win,
            text="Which product on the bottom is more similar to the product on top?\n(left = D, right = K)",
            color='black',
            height=24,
            pos=(0, 300)  # Position the prompt above all images
        )

        # Draw stimuli
        prompt.draw()
        reference_stim.draw()
        left_stim.draw()
        right_stim.draw()
        win.flip()

        # Collect response (not recorded)
        clock.reset()
        keys = event.waitKeys(keyList=['d', 'k', 'escape'], timeStamped=clock, maxWait=skip_time_limit)

        if keys:
            key, rt = keys[0]
            if key == 'escape':
                break  # Allow experimenter to quit
            else:
                # Highlight chosen image as feedback
                if key == 'd':  # Left choice
                    left_stim.color = [0.5, 0.5, 0.5]  # Dim the left image
                elif key == 'k':  # Right choice
                    right_stim.color = [0.5, 0.5, 0.5]  # Dim the right image

                # Draw feedback
                reference_stim.draw()
                left_stim.draw()
                right_stim.draw()
                win.flip()
                core.wait(0.5)  # Show feedback for 0.5 seconds
        else:
            # Trial was skipped
            missed_message.draw()
            win.flip()
            core.wait(2)  # Show missed message for 2 seconds

def run_similarity_trials(win, trial_list, writer, skip_time_limit, adaptive_mode):
    reference_image_path = 'images/trials/reference/ref_image.png'
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

    # Initialize ACJ system
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
        left_stim = visual.ImageStim(win, image=os.path.join('images/trials/comparison', left_image_name), size=(300, 300), pos=(-200, -100))
        right_stim = visual.ImageStim(win, image=os.path.join('images/trials/comparison', right_image_name), size=(300, 300), pos=(200, -100))

        # Create prompt above the images
        prompt = visual.TextStim(
            win,
            text="Which plant-based steak is more similar to the beef steak?\n(left = D, right = K)",
            color='black',
            height=24,
            pos=(0, 300)  # Position the prompt above all images
        )

        # Draw stimuli
        prompt.draw()
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
                writer.writerow([trial_num, left_image_name, right_image_name, key, rt])

                # Highlight chosen image as feedback
                if key == 'd':  # Left choice
                    left_stim.color = [0.5, 0.5, 0.5]  # Dim the left image
                elif key == 'k':  # Right choice
                    right_stim.color = [0.5, 0.5, 0.5]  # Dim the right image

                # Draw feedback
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
            writer.writerow([trial_num, left_image_name, right_image_name, "missing", "N/A"])
            continue
