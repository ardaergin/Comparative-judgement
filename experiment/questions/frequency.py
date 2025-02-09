from ..interface import Display

def ask_eat_frequency(display: Display):
    """
    Ask for the participant's frequency of plant-based meat alternative consumption
    using a multiple-choice prompt.
    
    Args:
        display (Display): An instance of the Display class.
        
    Returns:
        str: The selected frequency option.
    """
    question = ("How often do you eat plant-based meat alternatives?")
    options = [
        "Never",
        "Once every three months",
        "Once a month",
        "Once a week",
        "A couple of times per week",
        "Every day"
    ]
    return display.display_multiple_choice(question, options)
