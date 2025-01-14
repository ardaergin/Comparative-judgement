from psychopy import visual, event, core
import datetime

def get_participant_id(win, id_text, experiment_font):
    """
    Collect participant ID and append a timestamp to ensure unique filenames.

    Parameters:
        win: PsychoPy window object.
        id_text: Instruction text to prompt the participant for their ID.
        experiment_font: Font style for the displayed text.

    Returns:
        A unique participant ID with a timestamp, e.g., "participant1234_20250113_142530".
    """
    id_prompt = visual.TextStim(win, 
        text=id_text, 
        color='black', height=32, wrapWidth=800, pos=(0, 50),
        font=experiment_font,
        alignText='left', anchorHoriz='center'
    )
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
                    # Add timestamp to ID
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    return f"{participant_id}_{timestamp}"
            elif key == 'backspace':  # Remove the last character
                participant_id = participant_id[:-1]
            elif key in ['escape']:  # Allow experimenter to quit
                win.close()
                core.quit()
            else:
                participant_id += key
