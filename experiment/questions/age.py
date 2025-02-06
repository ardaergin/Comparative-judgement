import string
from ..interface import Display

def ask_age(display: Display):
    """
    Ask for the participant's age using a free text prompt.
    
    Args:
        display (Display): An instance of the Display class.
        
    Returns:
        str: The entered age.
    """
    def validate_age(input_text):
        try:
            age = int(input_text)
            return 16 <= age <= 99
        except ValueError:
            return False

    question = ("What is your age?\n"
                "(Please enter a number between 16 and 99 and press ENTER)")
    
    return display.free_text_prompt(question,
                                    validation_func=validate_age,
                                    allowed_chars=string.digits,
                                    max_length=2)
