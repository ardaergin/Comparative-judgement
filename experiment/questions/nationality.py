import string
from ..utils.nationality_list import COUNTRY_ADJECTIVALS
from ..interface import Display

def ask_nationality(display: Display):
    """
    Ask for the participant's nationality using a free text prompt.
    
    Args:
        display (Display): An instance of the Display class.
        
    Returns:
        str: The entered nationality.
    """
    # Create a set of valid nationalities (in lowercase) from the COUNTRY_ADJECTIVALS dictionary.
    valid_nationalities = set()
    for nationalities in COUNTRY_ADJECTIVALS.values():
        valid_nationalities.update(n.lower() for n in nationalities)
    
    def validate_nationality(input_text):
        return input_text.lower() in valid_nationalities

    question = ("What is your nationality?\n"
                "(Please enter your nationality and press ENTER)")
    # Allow lowercase letters, space, and hyphen.
    allowed = string.ascii_lowercase + " -"
    return display.free_text_prompt(question,
                                    validation_func=validate_nationality,
                                    allowed_chars=allowed)
