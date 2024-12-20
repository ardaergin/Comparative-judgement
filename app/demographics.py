from psychopy import visual, event, core
import csv

def collect_demographics(win, participant_id):
    """
    Collect demographic data: gender, age, and nationality.

    Parameters:
    - win: PsychoPy Window object
    - participant_id: Participant ID for saving demographic data

    Returns:
    - demographics: Dictionary of collected demographic data
    """
    demographics = {}

    # Gender
    gender_prompt = visual.TextStim(
        win,
        text="What is your gender?\n\nType your response and press ENTER (e.g., Male, Female, Non-binary, Prefer not to say).",
        height=24, wrapWidth=800, color='black', pos=(0, 50)
    )
    gender_response = visual.TextStim(win, text="", height=24, color='black', pos=(0, -50))

    demographics['gender'] = ""
    while True:
        gender_prompt.draw()
        gender_response.setText(demographics['gender'])  # Show current input
        gender_response.draw()
        win.flip()

        keys = event.waitKeys()
        for key in keys:
            if key == 'return' and demographics['gender']:  # Ensure non-empty input
                break
            elif key == 'backspace':  # Remove last character
                demographics['gender'] = demographics['gender'][:-1]
            elif key in ['escape']:  # Exit if needed
                win.close()
                core.quit()
            else:
                demographics['gender'] += key

        if 'return' in keys and demographics['gender']:
            break

    # Age
    age_prompt = visual.TextStim(
        win,
        text="What is your age?\n\nType your response and press ENTER.",
        height=24, wrapWidth=800, color='black', pos=(0, 50)
    )
    age_response = visual.TextStim(win, text="", height=24, color='black', pos=(0, -50))

    demographics['age'] = ""
    while True:
        age_prompt.draw()
        age_response.setText(demographics['age'])  # Show current input
        age_response.draw()
        win.flip()

        keys = event.waitKeys()
        for key in keys:
            if key == 'return' and demographics['age']:  # Ensure non-empty input
                break
            elif key == 'backspace':  # Remove last character
                demographics['age'] = demographics['age'][:-1]
            elif key in ['escape']:  # Exit if needed
                win.close()
                core.quit()
            elif key.isdigit():  # Ensure only numeric input
                demographics['age'] += key

        if 'return' in keys and demographics['age']:
            break

    # Nationality
    nationality_prompt = visual.TextStim(
        win,
        text="What is your nationality?\n\nType your response and press ENTER.",
        height=24, wrapWidth=800, color='black', pos=(0, 50)
    )
    nationality_response = visual.TextStim(win, text="", height=24, color='black', pos=(0, -50))

    demographics['nationality'] = ""
    while True:
        nationality_prompt.draw()
        nationality_response.setText(demographics['nationality'])  # Show current input
        nationality_response.draw()
        win.flip()

        keys = event.waitKeys()
        for key in keys:
            if key == 'return' and demographics['nationality']:  # Ensure non-empty input
                break
            elif key == 'backspace':  # Remove last character
                demographics['nationality'] = demographics['nationality'][:-1]
            elif key in ['escape']:  # Exit if needed
                win.close()
                core.quit()
            else:
                demographics['nationality'] += key

        if 'return' in keys and demographics['nationality']:
            break

    # Save Demographic Data
    with open(f"data/{participant_id}_demographics.csv", 'w', newline='') as demo_file:
        demo_writer = csv.writer(demo_file)
        demo_writer.writerow(['Gender', 'Age', 'Nationality'])
        demo_writer.writerow([demographics['gender'], demographics['age'], demographics['nationality']])

    return demographics
