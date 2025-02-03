from psychopy import visual, event, core
import string

def multiple_choice_prompt(win, question, options, font="Times New Roman"):
    """
    Displays a multiple-choice prompt and collects the response.

    Parameters:
    - win: PsychoPy window object
    - question: The question text.
    - options: A list of option strings.

    Returns:
    - response: The selected option.
    """
    question_prompt = visual.TextStim(
        win,
        text=question,
        height=24, wrapWidth=800, pos=(0, 200),
        color='black', font=font 
    )
    option_prompts = []
    for idx, option in enumerate(options):
        option_prompts.append(
            visual.TextStim(
                win,
                text=f"({idx + 1}) {option}",
                height=24,
                wrapWidth=800,
                color='black', font=font,
                pos=(0, 150 - idx * 50)  # Stack options vertically
            )
        )

    response = None
    while response is None:
        question_prompt.draw()
        for option_prompt in option_prompts:
            option_prompt.draw()
        win.flip()

        keys = event.waitKeys(keyList=[str(i) for i in range(1, len(options) + 1)] + ['escape'])
        if 'escape' in keys:
            win.close()
            core.quit()
        else:
            response = options[int(keys[0]) - 1]  # Map key to option

    return response


def free_text_prompt(win, question, validation_func=None, font="Times New Roman", allowed_chars=None, max_length=None):
    """
    Displays a free text prompt and collects the response, filtering unwanted keys.

    Parameters:
    - win: PsychoPy window object
    - question: The question text.
    - validation_func: A function to validate the input (optional).
    - font: Font for the text.
    - allowed_chars: A string of characters allowed in the input (optional).
                     If None, allows lowercase, uppercase letters, numbers, space, and common punctuation.
    - max_length: Maximum allowed length for the response (optional).

    Returns:
    - response: The validated input.
    """
    question_prompt = visual.TextStim(
        win,
        text=question,
        height=24, wrapWidth=800, pos=(0, 200),
        color='black', font=font
    )
    response_display = visual.TextStim(win, text="", height=24, color='black', pos=(0, 0))
    
    if allowed_chars is None:
        allowed_chars = set(string.ascii_letters + string.digits + string.punctuation + " ")
    else:
        allowed_chars = set(allowed_chars)

    response = ""
    while True:
        question_prompt.draw()
        response_display.setText(response)
        response_display.draw()
        win.flip()

        keys = event.waitKeys()
        for key in keys:
            if key == 'return':  # Enter key to submit
                if validation_func is None or validation_func(response):
                    return response
                else:
                    # Provide feedback for invalid input
                    response_display.setText("Invalid input, try again.")
                    response_display.draw()
                    win.flip()
                    core.wait(1)  # Wait for a second before continuing
            elif key == 'backspace':  # Remove the last character
                response = response[:-1]
            elif key == 'space':
                response += " "
            elif key in ['escape']:  # Allow experimenter to quit
                win.close()
                core.quit()
            elif key in ['lshift', 'rshift', 'lctrl', 'rctrl', 'lalt', 'ralt', 'up', 'down', 'left', 'right', 'capslock']:
                pass  # Explicitly ignore modifier keys
            elif len(key) == 1 and key in allowed_chars:
                if max_length is None or len(response) < max_length:
                    response += key
                else:
                    # Provide feedback for max length reached
                    response_display.setText("Max length reached.")
                    response_display.draw()
                    win.flip()
                    core.wait(1)  # Wait for a second before continuing
