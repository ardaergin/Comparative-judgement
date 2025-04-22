# experiment/core/stimulus.py
from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict
from psychopy import visual
import os
from PIL import Image

@dataclass
class Stimulus:
    """Represents a single stimulus image with intelligent scaling and unit conversion.
       The image is scaled to fit within a target box without changing its aspect ratio.
    """
    filename: str
    image_path: str
    target_height: int = 0.4
    win: Optional[visual.Window] = None
    psychopy_stim: Optional[visual.ImageStim] = None
    orig_width: int = field(init=False)
    orig_height: int = field(init=False)
    scaled_dimensions: Tuple[float, float] = field(init=False)

    def __post_init__(self):
        # 1. Get the original image dimensions in pixels.
        with Image.open(self.image_path) as img:
            self.orig_width, self.orig_height = img.size 
             # e.g., 400 x 300

        # 2. Get screen dimensions (in pixels) from the PsychoPy window.
        screen_width, screen_height = self.win.size  
        # e.g., 2000 x 1000

        # 3. Convert the original dimensions to height units.
        #    In height units, 1.0 equals the full window height.
        orig_width_h = self.orig_width / screen_height
        # 400 / 2000 = 0.2
        orig_height_h = self.orig_height / screen_height
        # 300 / 1000 = 0.3

        # 4. Determine which dimension is larger (in height units).
        if orig_width_h >= orig_height_h:
            max_dimension_h = orig_width_h
        else:
            max_dimension_h = orig_height_h

        # 5. Compute the scaling factor so that the largest side becomes target_height.
        scale_factor = self.target_height / max_dimension_h
        # e.g., 0.2 / 0.3 = 0.66

        # 6. Compute the scaled dimensions in height units.
        scaled_width = orig_width_h * scale_factor
        # e.g., 0.2 * 0.66 = 0.132
        scaled_height = orig_height_h * scale_factor
        self.scaled_dimensions = (scaled_width, scaled_height)

        # 7. Create the PsychoPy ImageStim using the computed scaled dimensions.
        if self.win is not None:
            self.psychopy_stim = visual.ImageStim(
                self.win,
                image=self.image_path,
                size=self.scaled_dimensions,
                units='height'
            )

    @property
    def id(self) -> str:
        """Unique identifier for the stimulus (filename without extension)"""
        return os.path.splitext(self.filename)[0]

    def set_position(self, position: Tuple[float, float], units: str = 'height'):
        """
        Set the position of the stimulus with flexible units.
        
        Args:
            position: (x, y) coordinates.
            units: The unit type ('height', 'norm', 'pix', etc.)
        """
        if self.psychopy_stim is None:
            raise ValueError("PsychoPy stimulus not initialized. Provide a window during creation.")
        self.psychopy_stim.units = units
        self.psychopy_stim.pos = position
