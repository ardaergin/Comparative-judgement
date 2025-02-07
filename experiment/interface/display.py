from dataclasses import dataclass
from typing import List, Optional, Dict, Union, Tuple, Callable
from pathlib import Path
from psychopy import visual, event, core
from PIL import Image
import string

@dataclass
class MultipleChoiceOption:
    """Represents a single multiple choice option."""
    text: str
    value: str  # The key the user should press to select this option.
    position: Tuple[float, float]

class Display:
    """Handles various types of visual presentations in the experiment."""
    
    def __init__(
        self,
        window: visual.Window,
        font: str = "Times New Roman",
        text_color: str = 'black',
        text_height: int = 0.03,
        wrap_width: int = 1,
        pos: Tuple[float, float] = (0, 0)
    ):
        self.window = window
        self.font = font
        self.text_color = text_color
        self.text_height = text_height
        self.wrap_width = wrap_width
        self.pos = pos  # default position for stimuli
        
        # Initialize common stimuli
        self._init_common_stimuli()
    
    def _init_common_stimuli(self):
        """Initialize commonly used stimuli."""
        self.continue_text = self._create_text_stimulus(
            "Press SPACE to continue", 
            position=(0, -0.45),
            Text_alignment='center'
        )
        self.enter_text = self._create_text_stimulus(
            "Press ENTER to submit response and continue", 
            position=(0, -0.45),
            Text_alignment='center'
        )
        self.escape_text = self._create_text_stimulus(
            "Press ESCAPE to quit", 
            position=(0, -0.45),
            Text_alignment='center'
        )
    
    def _safe_read_file(self, file_path: Union[str, Path]) -> str:
        """
        Safely read a text file, with centralized error handling.
        
        Args:
            file_path: Path to the text file.
            
        Returns:
            File contents as a string.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            self.quit_experiment()
    
    def _create_text_stimulus(
        self, 
        text: str, 
        position: Optional[Tuple[float, float]] = None,
        Text_alignment='left',
        Horizontal_anchor='center',
        **kwargs
    ) -> visual.TextStim:
        """
        Create a text stimulus without displaying it.
        
        Args:
            text: The text content.
            position: Optional position; defaults to self.pos.
            **kwargs: Additional TextStim parameters.
            
        Returns:
            A PsychoPy TextStim object.
        """
        pos = position if position is not None else self.pos
        kwargs.pop('pos', None)

        return visual.TextStim(
            win=self.window,
            text=text,
            height=self.text_height,
            color=self.text_color,
            font=self.font,
            wrapWidth=self.wrap_width,
            pos=pos,
            alignText=Text_alignment,
            anchorHoriz=Horizontal_anchor,
            **kwargs
        )
    
    def _create_image_stimulus(
        self,
        image_path: Union[str, Path],
        size: Optional[Tuple[float, float]] = None,
        position: Optional[Tuple[float, float]] = None
    ) -> visual.ImageStim:
        """
        Create an image stimulus without displaying it.
        
        If 'size' is provided, it is treated as a target maximum (width, height) in norm units.
        The image will be scaled to fit within that box without changing its aspect ratio.
        If 'size' is None, the image is loaded at its natural size (converted to norm units).
        """
        pos = position if position is not None else self.pos

        # Open the image to get its original dimensions in pixels.
        with Image.open(image_path) as img:
            orig_width, orig_height = img.size

        # Convert the original pixel size to norm units.
        # (Again, using the convention that 1 norm unit = win.size[1]/2 pixels)
        conversion_factor = self.window.size[1] / 2.0
        orig_width_norm = orig_width / conversion_factor
        orig_height_norm = orig_height / conversion_factor

        if size is None:
            # Use the image's natural size in norm units.
            norm_size = (orig_width_norm, orig_height_norm)
        else:
            # size is the maximum allowed (target) width and height in norm units.
            target_width, target_height = size
            scale_factor = min(target_width / orig_width_norm, target_height / orig_height_norm)
            norm_size = (orig_width_norm * scale_factor, orig_height_norm * scale_factor)

        return visual.ImageStim(
            self.window,
            image=str(image_path),
            size=norm_size,
            pos=pos,
            units='height'
        )
    
    def load_text(
        self, 
        text: str, 
        position: Optional[Tuple[float, float]] = None,
        **kwargs
    ) -> visual.TextStim:
        """
        Preload a text stimulus without displaying it.
        
        Args:
            text: The text content.
            position: Optional position.
            **kwargs: Additional TextStim parameters.
            
        Returns:
            A preloaded TextStim.
        """
        kwargs.pop('pos', None)
        return self._create_text_stimulus(text, position, **kwargs)
    
    def load_text_from_file(
        self, 
        file_path: Union[str, Path],
        position: Optional[Tuple[float, float]] = None,
        **kwargs
    ) -> visual.TextStim:
        """
        Load text from a file and return a preloaded TextStim.
        
        Args:
            file_path: Path to the text file.
            position: Optional position.
            **kwargs: Additional TextStim parameters.
            
        Returns:
            A preloaded TextStim.
        """
        kwargs.pop('pos', None)
        text = self._safe_read_file(file_path)
        return self._create_text_stimulus(text, position, **kwargs)
    
    def load_image(
        self,
        image_path: Union[str, Path],
        size: Optional[Tuple[int, int]] = None,
        position: Optional[Tuple[float, float]] = None
    ) -> visual.ImageStim:
        """
        Preload an image stimulus without displaying it.
        
        Args:
            image_path: Path to the image file.
            size: Optional (width, height); defaults to original image size.
            position: Optional position.
            
        Returns:
            A preloaded ImageStim.
        """
        return self._create_image_stimulus(image_path, size, position)
    
    def display_stimulus(
        self,
        stimulus: Union[visual.TextStim, visual.ImageStim],
        wait_for_space: bool = True,
        show_continue: bool = True,
        allow_escape: bool = False,
        keyList: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        Display a preloaded stimulus and wait for key press.
        
        Args:
            stimulus: Preloaded TextStim or ImageStim.
            wait_for_space: Whether to wait for a key press.
            show_continue: Whether to show continue prompt.
            allow_escape: Whether to allow quitting via escape.
            keyList: Optional list of keys to wait for.
            
        Returns:
            The key pressed.
        """
        stimulus.draw()
        if show_continue:
            self.continue_text.draw()
        if allow_escape:
            self.escape_text.draw()
        self.window.flip()
                
        if wait_for_space:
            keys = keyList if keyList is not None else ['space']
            if allow_escape and 'escape' not in keys:
                keys.append('escape')
            response = event.waitKeys(keyList=keys)
            if response and response[0] == 'escape':
                self.quit_experiment()
            return response[0] if response else None
        return None
                
    def display_multiple_choice(
        self,
        prompt: str,
        options: List[MultipleChoiceOption],
        prompt_pos: Optional[Tuple[float, float]] = None,
        show_continue: bool = False,
        allow_escape: bool = True
    ) -> Optional[str]:
        """
        Display a multiple-choice question.
        
        Args:
            prompt: The question prompt.
            options: A list of MultipleChoiceOption objects.
            prompt_pos: Position of the prompt text; defaults to (self.pos[0], self.pos[1]+200).
            show_continue: Whether to show the continue prompt.
            allow_escape: Whether to allow quitting via escape.
            
        Returns:
            The selected option's value.
        """
        prompt_position = prompt_pos if prompt_pos is not None else (self.pos[0], self.pos[1] + 200)
        prompt_stim = self._create_text_stimulus(prompt, prompt_position)
        
        # Draw each option
        for option in options:
            opt_stim = self._create_text_stimulus(option.text, option.position)
            opt_stim.draw()
        prompt_stim.draw()
        if show_continue:
            self.continue_text.draw()
        if allow_escape:
            self.escape_text.draw()
        self.window.flip()
        
        valid_keys = [opt.value for opt in options]
        if allow_escape:
            valid_keys.append('escape')
        response = event.waitKeys(keyList=valid_keys)
        if response and response[0] == 'escape':
            self.quit_experiment()
        return response[0] if response else None

    def free_text_prompt(
        self,
        question: str,
        validation_func: Optional[Callable[[str], bool]] = None,
        allowed_chars: Optional[str] = None,
        max_length: Optional[int] = None
    ) -> str:
        """
        Display a free text prompt and collect input.
        
        Args:
            question: The question to display.
            validation_func: Function to validate the response.
            allowed_chars: String of allowed characters.
            max_length: Maximum length of the response.
            
        Returns:
            The user's response.
        """
        question_stim = self._create_text_stimulus(question, (self.pos[0], self.pos[1] + 0.1))
        response_stim = self._create_text_stimulus("", self.pos)
        if allowed_chars is None:
            allowed_chars = set(string.ascii_letters + string.digits + string.punctuation + " ")
        else:
            allowed_chars = set(allowed_chars)
        
        response = ""
        while True:
            question_stim.draw()
            response_stim.setText(response)
            response_stim.draw()
            self.window.flip()
            
            keys = event.waitKeys()
            for key in keys:
                if key == 'return':
                    if validation_func is None or validation_func(response):
                        return response
                    else:
                        response_stim.setText("Invalid input, try again.")
                        response_stim.draw()
                        self.window.flip()
                        core.wait(1)
                        response = ""
                elif key == 'backspace':
                    response = response[:-1]
                elif key == 'space':
                    response += " "
                elif key == 'escape':
                    self.quit_experiment()
                elif len(key) == 1 and key in allowed_chars:
                    if max_length is None or len(response) < max_length:
                        response += key
                    else:
                        response_stim.setText("Max length reached.")
                        response_stim.draw()
                        self.window.flip()
                        core.wait(1)
        # (Loop ends via return upon valid input.)
    
    def display_likert(
        self,
        prompt: str,
        scale_points: int = 7,
        labels: Optional[Dict[int, str]] = None,
        prompt_pos: Optional[Tuple[float, float]] = None,
        scale_pos: Optional[Tuple[float, float]] = None,
        scale_width: float = 1,
        allow_escape: bool = True
    ) -> Optional[int]:
        """
        Display a Likert scale question.
        
        Args:
            prompt: The question prompt.
            scale_points: Number of points on the scale.
            labels: Optional dictionary mapping point numbers to label text.
            prompt_pos: Position of the prompt text; defaults to (self.pos[0], self.pos[1] + 200).
            scale_pos: Center position of the scale; defaults to self.pos.
            scale_width: Width of the scale in pixels.
            allow_escape: Whether to allow quitting via escape.
            
        Returns:
            The selected scale point as an integer.
        """
        prompt_position = prompt_pos if prompt_pos is not None else (self.pos[0], self.pos[1] + 200)
        scale_center = scale_pos if scale_pos is not None else self.pos
        
        prompt_stim = self._create_text_stimulus(prompt, prompt_position)
        
        line = visual.Line(
            self.window,
            start=(-scale_width/2, scale_center[1]),
            end=(scale_width/2, scale_center[1]),
            lineColor=self.text_color
        )
        
        point_stims = []
        spacing = scale_width / (scale_points - 1)
        for i in range(scale_points):
            x = -scale_width/2 + i * spacing
            point = visual.Circle(
                self.window,
                radius=10,
                pos=(x, scale_center[1]),
                fillColor=self.text_color
            )
            number = self._create_text_stimulus(str(i + 1), (x, scale_center[1] - 30))
            label = None
            if labels and (i + 1) in labels:
                label = self._create_text_stimulus(labels[i + 1], (x, scale_center[1] - 60))
            point_stims.append((point, number, label))
        
        prompt_stim.draw()
        line.draw()
        for point, number, label in point_stims:
            point.draw()
            number.draw()
            if label:
                label.draw()
        if allow_escape:
            self.escape_text.draw()
        self.window.flip()
        
        valid_keys = [str(i) for i in range(1, scale_points + 1)]
        if allow_escape:
            valid_keys.append('escape')
        response = event.waitKeys(keyList=valid_keys)
        if response and response[0] == 'escape':
            self.quit_experiment()
        return int(response[0]) if response else None

    def display_error(
        self,
        message: str,
        duration: float = 2.0
    ):
        """
        Display an error message briefly.
        
        Args:
            message: The error message to display.
            duration: Duration in seconds.
        """
        error_stim = self._create_text_stimulus(message, (0, 0), color='red')
        error_stim.draw()
        self.window.flip()
        core.wait(duration)
    
    def quit_experiment(self):
        """Clean up and exit the experiment."""
        self.window.close()
        core.quit()
