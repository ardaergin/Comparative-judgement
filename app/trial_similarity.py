from psychopy import visual, core, event
import os
from app.adaptive_algorithm import ACJ


def run_practice(win, trial_list, skip_time_limit):
    reference_image_path = 'images_practice/reference/ref_image.jpg'
    reference_stim = visual.ImageStim(win, image=reference_image_path, size=(300, 300), pos=(0, 200))
    fixation = visual.TextStim(win, text="+", height=50, color='black')

    clock = core.Clock()

    for trial_num, (left_image_name, right_image_name) in enumerate(trial_list, start=1):
        # Show fixation point
        fixation.draw()
        win.flip()
        core.wait(1)

        # Create image stimuli
        left_stim = visual.ImageStim(win, image=os.path.join('images_practice/comparison', left_image_name), size=(300, 300), pos=(-200, -100))
        right_stim = visual.ImageStim(win, image=os.path.join('images_practice/comparison', right_image_name), size=(300, 300), pos=(200, -100))

        # Draw stimuli
        reference_stim.draw()
        left_stim.draw()
        right_stim.draw()

        prompt = visual.TextStim(
            win,
            text="Which is more similar to the reference image?\nLeft (←) or Right (→)",
            color='black',
            height=24,
            pos=(0, -300)
        )
        prompt.draw()
        win.flip()

        # Collect response (not recorded)
        clock.reset()
        keys = event.waitKeys(keyList=['left', 'right', 'escape'], timeStamped=clock, maxWait=skip_time_limit)

        if keys and keys[0][0] == 'escape':
            break  # Allow experimenter to quit practice round


def run_similarity_trials(win, trial_list, writer, skip_time_limit, adaptive_mode):
    reference_image_path = 'images/reference/ref_image.png'
    reference_stim = visual.ImageStim(win, image=reference_image_path, size=(300, 300), pos=(0, 200))
    fixation = visual.TextStim(win, text="+", height=50, color='black')

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
        left_stim = visual.ImageStim(win, image=os.path.join('images/comparison', left_image_name), size=(300, 300), pos=(-200, -100))
        right_stim = visual.ImageStim(win, image=os.path.join('images/comparison', right_image_name), size=(300, 300), pos=(200, -100))

        # Draw stimuli
        reference_stim.draw()
        left_stim.draw()
        right_stim.draw()

        prompt = visual.TextStim(win, text="Which is more similar to the reference image?\nLeft ( ← ) or Right ( → ) ", color='black', height=24, pos=(0, -300))
        prompt.draw()
        win.flip()

        # Collect response
        clock.reset()
        keys = event.waitKeys(keyList=['left', 'right', 'escape'], timeStamped=clock, maxWait=skip_time_limit)

        if keys:
            key, rt = keys[0]
            if key == 'escape':
                break
            else:
                winner = left_image_name if key == 'left' else right_image_name
                writer.writerow([trial_num, left_image_name, right_image_name, key, rt])

                if adaptive_mode:
                    acj.record_comparison(left_image_name, right_image_name, winner)
                    acj.update_parameters()
        else:
            writer.writerow([trial_num, left_image_name, right_image_name, "missing", "N/A"])
            continue
