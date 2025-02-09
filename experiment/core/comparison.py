from dataclasses import dataclass
from typing import Optional
from .stimulus import Stimulus

@dataclass
class Comparison:
    """
    Represents a pair of stimuli for comparison
    """
    left_stimuli: Stimulus
    right_stimuli: Stimulus
    trial_position: Optional[int] = None  # position in trial sequence
    _hash: Optional[int] = None

    def __post_init__(self):
        """
        Create a stable hash for this comparison pair.
        This ensures same pairs get same hash regardless of order.
        """
        self._hash = hash(tuple(sorted([self.left_stimuli.filename, self.right_stimuli.filename])))
    
    def __hash__(self):
        return self._hash
    
    def __eq__(self, other):
        if not isinstance(other, Comparison):
            return NotImplemented
        return hash(self) == hash(other)

    def swap(self) -> 'Comparison':
        """Create new pair with swapped positions"""
        return Comparison(self.right_stimuli, self.left_stimuli)
    
    @property
    def id(self) -> str:
        """Unique identifier for the pair"""
        return f"{self.left_stimuli.id}_vs_{self.right_stimuli.id}"

    @property
    def order_indicator(self) -> int:
        """
        Returns an indicator of the ordering:
        - Returns 1 if the left image is the first in sorted order,
        - Returns 2 if the left image is the second in sorted order.
        
        This tells you whether the comparison was, for example,
        'img1-img2' (1) or 'img2-img1' (2) relative to the sorted order.
        """
        sorted_files = sorted([self.left_stimuli.filename, self.right_stimuli.filename])
        return 1 if self.left_stimuli.filename == sorted_files[0] else 2
