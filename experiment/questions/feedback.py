from psychopy import visual, event, core
from ..interface import Display

def ask_feedback(display: Display):
    """
    Collect feedback from participants using a multi-line TextBox2,
    and return the entered feedback as a string.
    
    Parameters:
        display: An instance of your Display class.
        
    Returns:
        str: The participant's feedback.
    """
    # Get the underlying window from the Display instance
    win = display.window

    # The text to use
    with open("texts/8_comment_screen.txt", "r") as file:
        comment_text = file.read()
    instruction_text_stim = visual.TextStim(
        win,
        text=comment_text,
        font=display.font,
        height=display.text_height,
        wrapWidth=1,
        color='black',
        pos=(0, 0.3),
        alignText='center'
    )

    # Create a multi-line TextBox2 for feedback.
    feedback_box = visual.TextBox2(
        win,
        text="",
        font=display.font,
        letterHeight=display.text_height,
        size=(0.8, 0.3),
        pos=(0, 0),
        color=display.text_color,
        fillColor='white',
        borderColor='black',
        editable=True,
        anchor='center',
        units='height'
    )
    
    # Create a "Finish" button using a TextStim.
    next_button = visual.TextStim(
        win,
        text="Finish",
        height=display.text_height,
        color='black',
        pos=(0, -0.4)
    )
    # Create a clickable area (a rectangular button) for the finish button.
    button_box = visual.Rect(
        win,
        width=0.3,
        height=0.1,
        pos=(0, -0.4),
        fillColor=None,
        lineColor='black',
        units='height'
    )
    mouse = event.Mouse(visible=True, win=win)
    
    # Feedback collection loop.
    while True:
        # Draw the static instruction text.        
        instruction_text_stim.draw()
        
        # Draw the editable feedback textbox.
        feedback_box.draw()
        
        # Draw the finish button and its clickable area.
        button_box.draw()
        next_button.draw()
        
        win.flip()
        
        # Check for mouse click on the Finish button.
        if mouse.getPressed()[0]:  # left button pressed
            if mouse.getPressed()[0]:
                if button_box.contains(mouse.getPos()):
                    return feedback_box.text
        
        # Check for the escape key using your Display's built-in mechanism.
        keys = event.getKeys()
        if 'escape' in keys:
            display.quit_experiment()
