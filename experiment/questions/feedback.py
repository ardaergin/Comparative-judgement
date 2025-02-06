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
    win = display.window  # Get the underlying window from the Display instance

    # Instructions for providing feedback.
    instruction_text = (
        "This was the end of this session, thank you very much for your participation!\n\n"
        "If you have any remarks, questions or feedback regarding this study, "
        "please enter them below. It will be really helpful for us to know how "
        "you made your decisions. If not, you can just click on the 'Finish' button."
    )
    
    # Display the instructions (non-blocking).
    display.display_text(instruction_text, position=(0, 200), wait_for_space=False)
    
    # Create a multi-line TextBox2 for feedback.
    feedback_box = visual.TextBox2(
        win,
        text="",
        font="Arial",
        letterHeight=24,
        size=(600, 200),  # width, height in pixels
        pos=(0, 0),
        color='black',
        fillColor='white',
        borderColor='black',
        editable=True,
        anchor='center'
    )
    
    # Create a "Finish" button using a TextStim.
    next_button = visual.TextStim(
        win,
        text="Finish",
        height=24,
        color='black',
        pos=(0, -200)
    )
    
    # Create a clickable area (a rectangular button) for the finish button.
    button_box = visual.Rect(
        win,
        width=100,
        height=50,
        pos=(0, -200),
        fillColor=None,
        lineColor='black'
    )
    
    mouse = event.Mouse(visible=True, win=win)
    
    # Feedback collection loop.
    while True:
        # Draw the static instruction text.
        instruction_text_stim = visual.TextStim(
            win,
            text=instruction_text,
            height=24,
            wrapWidth=800,
            color='black',
            pos=(0, 200),
            alignText='center'
        )
        instruction_text_stim.draw()
        
        # Draw the editable feedback textbox.
        feedback_box.draw()
        
        # Draw the finish button and its clickable area.
        button_box.draw()
        next_button.draw()
        
        win.flip()
        
        # Check for mouse click on the Finish button.
        if mouse.getPressed()[0]:  # left button pressed
            if button_box.contains(mouse.getPos()):
                # Return the entered feedback.
                feedback_text = feedback_box.text
                return feedback_text
        
        # Check for the escape key using your Display's built-in mechanism.
        keys = event.getKeys()
        if 'escape' in keys:
            display.quit_experiment()
