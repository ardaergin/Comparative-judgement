from typing import Tuple, Union
from psychopy import visual

class UnitConverter:
    """Utility class to convert sizes between different PsychoPy units"""
    @staticmethod
    def pixels_to_height(win: visual.Window, pixels: Union[int, Tuple[int, int]]) -> Union[float, Tuple[float, float]]:
        """
        Convert pixel dimensions to height units
        """
        if isinstance(pixels, int):
            return pixels / win.size[1]
        
        width, height = pixels
        return (
            width / win.size[1],   # width in height units
            height / win.size[1]   # height in height units
        )
    
    @staticmethod
    def pixels_to_norm(win: visual.Window, pixels: Union[int, Tuple[int, int]]) -> Union[float, Tuple[float, float]]:
        """
        Convert pixel dimensions to normalized units
        """
        if isinstance(pixels, int):
            return pixels / (win.size[1] / 2)
        
        width, height = pixels
        return (
            width / (win.size[1] / 2),   # width in norm units
            height / (win.size[1] / 2)   # height in norm units
        )
