from psychopy import visual, core
from datetime import datetime
from app.utils import free_text_prompt

def get_participant_id(win, id_text, experiment_font):
    """
    Collect participant ID and append a timestamp to ensure unique filenames.

    Parameters:
        win: PsychoPy window object.
        id_text: Instruction text to prompt the participant for their ID.
        experiment_font: Font style for the displayed text.

    Returns:
        A unique participant ID with a timestamp, e.g., "participant1234_20250113_142530".
    """
    def validate_id(input_text):
        return len(input_text) > 0  # Ensure non-empty input

    participant_id = free_text_prompt(win, id_text, validation_func=validate_id)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{participant_id}_{timestamp}"
