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
    gender_question = "What is your gender?\n(Please press the number on the left keyboard corresponding to your chosen options. Do not use the keyboard on the right.)\n "
    gender_options = ["Male", "Female", "Non-binary", "Prefer not to say"]
    demographics['gender'] = multiple_choice_prompt(win, gender_question, gender_options)

    # Age
    def validate_age(input_text):
        try:
            age = int(input_text)
            return 16 <= age <= 99
        except ValueError:
            return False

    age_question = "What is your age?\n(Please enter a number between 16 and 99 and press ENTER)"
    demographics['age'] = free_text_prompt(win, age_question, validation_func=validate_age)

    # Nationality
    nationality_question = "What is your nationality?\n (Please enter your nationality and press ENTER)\n "
    demographics['nationality'] = free_text_prompt(win, nationality_question, validation_func=None)

    # Dietary preference
    dietary_question = "How would you describe your diet?\n(Please press the number on the left keyboard corresponding your chosen option. Do not use the keyboard on the right.)\n"
    dietary_options = [
        "Omnivore (I eat animal products)",
        "Vegetarian",
        "Vegan",
        "Pescatarian",
        "Other"
    ]
    demographics['diet'] = multiple_choice_prompt(win, dietary_question, dietary_options)

    # Frequency of plant-based meat alternative eating
    eat_frequency_question = "How often do you eat plant-based meat alternatives?\n(Please press the number on the left keyboard corresponding to your chosen option. Do not use the keyboard on the right.)\n "
    eat_frequency_options = [
        "Never",
        "Once every three months",
        "Once a month",
        "Once a week",
	    "A couple of times per week",
        "Every day"
    ]
    demographics['eat_frequency'] = multiple_choice_prompt(win, eat_frequency_question, eat_frequency_options)

    # Save Demographic Data
    with open(f"data/{participant_id}_demographics.csv", 'w', newline='') as demo_file:
        demo_writer = csv.writer(demo_file)
        demo_writer.writerow(['Gender', 'Age', 'Nationality', 'Diet', 'Eat Frequency'])
        demo_writer.writerow([
            demographics['gender'],
            demographics['age'],
            demographics['nationality'],
            demographics['diet'],
            demographics['eat_frequency']
        ])

    return demographics
