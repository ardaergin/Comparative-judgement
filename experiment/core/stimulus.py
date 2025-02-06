from dataclasses import dataclass, field
from typing import Optional, Tuple
from psychopy import visual
import os
from PIL import Image
import os
from ..utils import UnitConverter

@dataclass
class Stimulus:
    """Represents a single stimulus image with intelligent scaling and unit conversion"""
    filename: str
    image_path: str
    target_size_px: Tuple[int, int] = (300, 300)
    win: Optional[visual.Window] = None
    psychopy_stim: Optional[visual.ImageStim] = None
    original_dimensions: Tuple[int, int] = field(init=False)
    scaled_dimensions: Tuple[int, int] = field(init=False)

    def __post_init__(self):
        """
        Post-initialization method to:
        1. Get original image dimensions
        2. Calculate scaled dimensions 
        3. Create PsychoPy ImageStim with proper scaling
        """
        # Get original image dimensions
        with Image.open(self.image_path) as img:
            self.original_dimensions = img.size

        # Calculate scaled dimensions to fit target size while maintaining aspect ratio
        orig_width, orig_height = self.original_dimensions
        target_width, target_height = self.target_size_px

        # Calculate scaling factors
        width_ratio = target_width / orig_width
        height_ratio = target_height / orig_height
        
        # Choose the smaller scaling factor to fit within target box
        scale_factor = min(width_ratio, height_ratio)
        
        # Calculate new dimensions
        scaled_width = int(orig_width * scale_factor)
        scaled_height = int(orig_height * scale_factor)
        
        self.scaled_dimensions = (scaled_width, scaled_height)

        # Create PsychoPy ImageStim if window is provided
        # This essentially preloads the images
        if self.win is not None:
            self.psychopy_stim = visual.ImageStim(
                self.win, 
                image=self.image_path,
                # Defaulting to height units for better screen compatibility:
                size=self.get_size_in_units('pix'),
                units='pix'
            )

    @property
    def id(self) -> str:
        """Unique identifier for the stimulus (filename without extension)"""
        return os.path.splitext(self.filename)[0]

    def get_size_in_units(self, units: str = 'pix') -> Tuple[float, float]:
        """
        Get scaled image size in specified units
        
        Args:
            units: Target units ('height', 'norm', 'pix')
        
        Returns:
            Size in specified units
        """
        if self.win is None:
            raise ValueError("Window must be provided to convert units")
        
        if units == 'pix':
            return self.scaled_dimensions
        elif units == 'height':
            return UnitConverter.pixels_to_height(self.win, self.scaled_dimensions)
        elif units == 'norm':
            return UnitConverter.pixels_to_norm(self.win, self.scaled_dimensions)
        else:
            raise ValueError(f"Unsupported units: {units}")

    def set_position(self, position: Tuple[float, float], units: str = 'pix'):
        """
        Set position of the stimulus with flexible units
        
        Args:
            position: (x, y) coordinates
            units: psychopy units (height, norm, pix, etc.)
        """
        if self.psychopy_stim is None:
            raise ValueError("PsychoPy stimulus not initialized. Provide a window during creation.")
        
        self.psychopy_stim.units = units
        self.psychopy_stim.pos = position
