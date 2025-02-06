from ..interface import Display

def ask_diet(display: Display):
    """
    Ask for the participant's dietary preference using a multiple-choice prompt.
    
    Args:
        display (Display): An instance of the Display class.
        
    Returns:
        str: The selected dietary option.
    """
    question = ("How would you describe your diet?\n"
                "(Please press the number corresponding to your chosen option.)")
    options = [
        "Omnivore (I eat animal products)",
        "Vegetarian",
        "Vegan",
        "Pescatarian",
        "Other"
    ]
    
    return display.multiple_choice_prompt(question, options)
