from psychopy import visual, core
import csv
from app.utils import multiple_choice_prompt, free_text_prompt

def collect_demographics(win, participant_id):
    """
    Collect demographic data using multiple-choice questions and free text input.

    Parameters:
    - win: PsychoPy Window object
    - participant_id: Participant ID for saving demographic data

    Returns:
    - demographics: Dictionary of collected demographic data
    """
    demographics = {}

    # Gender
    gender_question = "What is your gender?"
    gender_options = ["Male", "Female", "Non-binary", "Prefer not to say"]
    demographics['gender'] = multiple_choice_prompt(win, gender_question, gender_options)

    # Age
    def validate_age(input_text):
        try:
            age = int(input_text)
            return 16 <= age <= 99
        except ValueError:
            return False

    age_question = "What is your age? (Please enter a number between 16 and 99)"
    demographics['age'] = free_text_prompt(win, age_question, validation_func=validate_age)

    # Nationality
    nationality_question = "What is your nationality?"
    demographics['nationality'] = free_text_prompt(win, nationality_question, validation_func=None)

    # Dietary preference
    dietary_question = "How would you describe your diet?"
    dietary_options = [
        "Omnivore (I eat animal products)",
        "Vegetarian",
        "Vegan",
        "Pescatarian",
        "Other"
    ]
    demographics['diet'] = multiple_choice_prompt(win, dietary_question, dietary_options)

    # Frequency of plant-based meat alternative purchase
    purchase_frequency_question = ("How often do you purchase plant-based meat alternatives?")
    purchase_frequency_options = [
        "Less than once a month",
        "At least once a month, but less than once a week",
        "Once or twice a week",
        "More than twice a week, but less than everyday",
        "At least once a day"
    ]
    demographics['purchase_frequency'] = multiple_choice_prompt(win, purchase_frequency_question, purchase_frequency_options)

    # Save Demographic Data
    with open(f"data/{participant_id}_demographics.csv", 'w', newline='') as demo_file:
        demo_writer = csv.writer(demo_file)
        demo_writer.writerow(['Gender', 'Age', 'Nationality', 'Diet', 'Purchase Frequency'])
        demo_writer.writerow([
            demographics['gender'],
            demographics['age'],
            demographics['nationality'],
            demographics['diet'],
            demographics['purchase_frequency']
        ])

    return demographics
