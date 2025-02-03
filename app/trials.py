from psychopy import visual, core, event
import random

def run_trials(
    win, 
    trial_list, 
    writer=None, 
    skip_time_limit=4, 
    prompt_text="Which is more similar to the reference image?\n(left = D, right = K)", 
    comparison_images=None,  
    reference_image=None,    
    round_type="unknown",
    num_breaks=0,           
    break_wait_time=20      # <-- NEW: how many seconds to wait before letting them press space
):
    """
    General function to run trials, with optional breaks that display block info.

    Parameters:
        win: PsychoPy Window object.
        trial_list: List of trials (pairs of images).
        writer: CSV writer object for saving responses (optional).
        skip_time_limit: Time in seconds before a trial is skipped.
        prompt_text: Prompt text to display above the images.
        image_folder: Path to the folder containing comparison images.
        comparison_images: Dictionary of preloaded comparison ImageStim objects.
        reference_image: Preloaded reference ImageStim object.
        round_type: String specifying the type of the round (e.g., "practice", "similarity", "liking").
        num_breaks: Integer, how many breaks to give during this block of trials (0 = no breaks).
        break_wait_time: How many seconds to wait on the break screen before continuing.
    """

    # Use preloaded reference image
    reference_stim = reference_image

    # Fixation stimulus
    fixation = visual.TextStim(win, text="+", height=50, color='black', pos=(0, 0))

    # Missed trial message
    missed_message = visual.TextStim(
        win,
        text="You missed the last trial.\nPlease respond faster.\n\n"
             "We are interested in your initial impressions.\n\n"
             "Press the SPACE BAR to continue.",
        color='black',
        height=24,
        wrapWidth=800,
        pos=(0, 0)
    )

    clock = core.Clock()

    # Number of trials and number of blocks
    n_trials = len(trial_list)
    n_blocks = num_breaks + 1  # e.g. 2 breaks -> 3 blocks

    # If num_breaks=0, effectively no intermediate breaks
    if n_blocks > 1:
        block_size = n_trials // n_blocks  # integer division
    else:
        block_size = n_trials

    for trial_index, (pair_left, pair_right) in enumerate(trial_list):
        trial_num = trial_index + 1

        # Random 50% swap
        if random.choice([True, False]):
            pair_left, pair_right = pair_right, pair_left

        # Show fixation
        fixation.draw()
        win.flip()
        core.wait(0.5)

        # Grab preloaded images
        left_stim = comparison_images[pair_left]
        right_stim = comparison_images[pair_right]

        # Positions
        if round_type == "liking":
            left_stim.pos = (-250, 0)
            right_stim.pos = (250, 0)
        else:
            left_stim.pos = (-250, -150)
            right_stim.pos = (250, -150)

        # Prompt
        prompt = visual.TextStim(
            win,
            text=prompt_text,
            color='black',
            height=24,
            pos=(0, 350)
        )

        # Draw stimuli
        prompt.draw()
        if reference_stim and round_type != "liking":
            reference_stim.draw()
        left_stim.draw()
        right_stim.draw()
        win.flip()

        # Collect response
        clock.reset()
        keys = event.waitKeys(
            keyList=['d', 'k', 'escape'],
            timeStamped=clock,
            maxWait=skip_time_limit
        )

        if keys:
            key, rt = keys[0]
            if key == 'escape':
                break  # Allow experimenter to quit
            else:
                winner = pair_left if key == 'd' else pair_right

                # Save data if writer is provided
                if writer:
                    writer.writerow([trial_num, round_type, pair_left, pair_right, key, rt])

                # Highlight chosen image
                chosen_stim = left_stim if key == 'd' else right_stim
                blue_border = visual.Rect(
                    win,
                    width=chosen_stim.size[0] + 10,
                    height=chosen_stim.size[1] + 10,
                    lineColor='blue',
                    lineWidth=5,
                    pos=chosen_stim.pos
                )

                # Feedback for 0.5s
                prompt.draw()
                if reference_stim:
                    reference_stim.draw()
                left_stim.draw()
                right_stim.draw()
                blue_border.draw()
                win.flip()
                core.wait(0.5)

        else:
            # Missed trial
            missed_message.draw()
            win.flip()
            event.waitKeys(keyList=['space'])
            if writer:
                writer.writerow([trial_num, round_type, pair_left, pair_right, "missing", "N/A"])

        # ---- NEW/UPDATED: Show break screen if needed ----
        # We'll show a break after every 'block_size' trials, except for the last block
        if n_blocks > 1:  # Only if we actually have breaks
            # Check if we completed a block boundary
            if (trial_num % block_size == 0) and (trial_num < n_trials):
                # We have completed block # = trial_num//block_size
                current_block = trial_num // block_size
                # NOTE: The last block is block index = n_blocks, we skip break if current_block == n_blocks.
                if current_block < n_blocks:  
                    # e.g., "Block 1 / 3 is done. Please take a ~20s break..."
                    break_text = (f"Block {current_block} of {n_blocks} completed.\n\n"
                                  f"Please take a short break (~{break_wait_time} s).\n"
                                  "Press SPACE when you are ready to continue.")
                    break_stim = visual.TextStim(
                        win, 
                        text=break_text,
                        color='black',
                        height=24,
                        wrapWidth=800,
                        pos=(0, 0)
                    )
                    break_stim.draw()
                    win.flip()
                    
                    # Wait the specified break time (optional)
                    core.wait(break_wait_time)
                    
                    # Then wait for SPACE
                    event.waitKeys(keyList=['space'])

    # End of function
