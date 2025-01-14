from psychopy import visual, event, core

def multiple_choice_prompt(win, question, options):
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
        height=24, wrapWidth=800, color='black', pos=(0, 200)
    )
    option_prompts = []
    for idx, option in enumerate(options):
        option_prompts.append(
            visual.TextStim(
                win,
                text=f"({idx + 1}) {option}",
                height=24,
                wrapWidth=800,
                color='black',
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


def free_text_prompt(win, question, validation_func=None):
    """
    Displays a free text prompt and collects the response.

    Parameters:
    - win: PsychoPy window object
    - question: The question text.
    - validation_func: A function to validate the input (optional).

    Returns:
    - response: The validated input.
    """
    question_prompt = visual.TextStim(
        win,
        text=question,
        height=24, wrapWidth=800, color='black', pos=(0, 200)
    )
    response_display = visual.TextStim(win, text="", height=24, color='black', pos=(0, 0))

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
            elif key == 'backspace':  # Remove the last character
                response = response[:-1]
            elif key in ['escape']:  # Allow experimenter to quit
                win.close()
                core.quit()
            else:
                response += key
