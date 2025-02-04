from psychopy import visual, event, core
import csv
from datetime import datetime

def collect_feedback(win, participant_id):
    """
    Collect and save feedback from participants using a multi-line TextBox2.
    
    Parameters:
        win: PsychoPy window object
        participant_id: Participant ID for saving feedback data
    """
    # Create instruction text
    instruction_text = ("This was the end of this session, thank you very much for your participation!\n\n"
                       "If you have any remarks, questions or feedback regarding this study, "
                       "please enter them below. It will be really helpful for us to know how "
                       "you made your decisions. If not, you can just click on the 'Finish' button.")
    
    instructions = visual.TextStim(
        win,
        text=instruction_text,
        height=24,
        wrapWidth=800,
        color='black',
        pos=(0, 200),
        alignText='center'
    )
    
    # Create text box for feedback
    feedback_box = visual.TextBox2(
        win,
        text="",
        font="Arial",
        letterHeight=24,
        size=(600, 200),  # width, height
        pos=(0, 0),
        color='black',
        fillColor='white',
        borderColor='black',
        editable=True,
        anchor='center'
    )
    
    # Create "Next" button
    next_button = visual.TextStim(
        win,
        text="Finish",
        height=24,
        color='black',
        pos=(0, -200)
    )
    
    # Create button box for click detection
    button_box = visual.Rect(
        win,
        width=100,
        height=50,
        pos=(0, -200),
        fillColor=None,
        lineColor='black'
    )
    
    mouse = event.Mouse()
    
    while True:
        instructions.draw()
        feedback_box.draw()
        button_box.draw()
        next_button.draw()
        win.flip()
        
        # Check for mouse clicks on the Next button
        if mouse.getPressed()[0]:  # Left mouse button
            if button_box.contains(mouse.getPos()):
                # Save feedback to file
                feedback_text = feedback_box.text
                with open(f"data/{participant_id}_comments.csv", 'w', newline='', encoding='utf-8') as feedback_file:
                    feedback_writer = csv.writer(feedback_file)
                    feedback_writer.writerow(['Timestamp', 'Feedback'])
                    feedback_writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), feedback_text])
                return
        
        # Check for escape key
        keys = event.getKeys()
        if 'escape' in keys:
            win.close()
            core.quit()

# Final thank you message
def show_final_message(win):
    """
    Display final thank you message.
    
    Parameters:
        win: PsychoPy window object
    """
    thank_you = visual.TextStim(
        win,
        text="Thank you for your participation! The study is over, you can leave your cubicle now.",
        height=24,
        color='black'
    )
    thank_you.draw()
    win.flip()
    core.wait(10)
