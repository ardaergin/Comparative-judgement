from psychopy import visual, event, core

def get_participant_id(win):
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
                    return participant_id
            elif key == 'backspace':  # Remove the last character
                participant_id = participant_id[:-1]
            elif key in ['escape']:  # Allow experimenter to quit
                win.close()
                core.quit()
            else:
                participant_id += key
