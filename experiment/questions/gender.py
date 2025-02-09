from ..interface import Display

def ask_gender(display: Display):
    """
    Ask for the participant's gender using a multiple-choice prompt.
    
    Args:
        display (Display): An instance of the Display class.
    
    Returns:
        str: The selected gender option.
    """
    
    question = ("What is your gender?")
    options = ["Male", "Female", "Non-binary", "Prefer not to say"]
    
    return display.display_multiple_choice(question, options)
