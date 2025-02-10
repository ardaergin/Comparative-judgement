from ..interface import Display

def ask_diet(display: Display):
    """
    Ask for the participant's dietary preference using a multiple-choice prompt.
    
    Args:
        display (Display): An instance of the Display class.
        
    Returns:
        str: The selected dietary option.
    """
    question = ("How would you describe your diet?")
    options = [
        "Omnivore (I eat animal products)",
        "Vegetarian (I do not eat meat nor fish, but I eat dairy products)",
        "Vegan (I do not eat meat, fish nor dairy products)",
        "Pescatarian (I eat fish but not meat)",
        "Other"
    ]
    
    return display.display_multiple_choice(question, options)
