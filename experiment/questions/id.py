import string
from ..interface import Display

def ask_id(display: Display) -> str:
    """
    Collect participant ID using the Display's free text prompt.

    Parameters:
        display (Display): An instance of the Display class.
        id_text (str): Instruction text to prompt the participant for their ID.

    Returns:
        str: A unique participant ID.
    """
    with open("texts/2_participant_id.txt", "r") as file:
        id_text = file.read()

    def validate_id(input_text):
        return len(input_text) == 5 and input_text.isdigit()

    participant_id = display.free_text_prompt(
        id_text,
        validation_func=validate_id,
        allowed_chars=string.digits,
        max_length=5
    )

    return participant_id
