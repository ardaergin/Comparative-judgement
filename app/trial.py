from psychopy import visual, core, event
import os

def run_trials(win, trial_list, writer, skip_time_limit):
    reference_image_path = 'images/reference/ref_image.png'
    reference_stim = visual.ImageStim(win, image=reference_image_path, size=(300, 300), pos=(0, 200))
    fixation = visual.TextStim(win, text="+", height=50, color='black')

    clock = core.Clock()
    for trial_num, (left_image_name, right_image_name) in enumerate(trial_list, start=1):
        # Show fixation point
        fixation.draw()
        win.flip()
        core.wait(1)  # Display fixation for 1 second
        
        # Create image stimuli for this trial
        left_stim = visual.ImageStim(win, image=os.path.join('images/comparison', left_image_name), size=(300, 300), pos=(-200, -100))
        right_stim = visual.ImageStim(win, image=os.path.join('images/comparison', right_image_name), size=(300, 300), pos=(200, -100))
        
        # Draw the stimuli
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
        
        # Collect response
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
