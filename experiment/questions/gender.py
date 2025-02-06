from ..interface import Display

def ask_gender(display: Display):
    """
    Ask for the participant's gender using a multiple-choice prompt.
    
    Args:
        display (Display): An instance of the Display class.
    
    Returns:
        str: The selected gender option.
    """
    
    question = ("What is your gender?\n"
                "(Please press the number corresponding to your chosen option.)")
    options = ["Male", "Female", "Non-binary", "Prefer not to say"]
    
    return display.multiple_choice_prompt(question, options)
