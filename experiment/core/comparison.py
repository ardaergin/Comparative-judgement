from dataclasses import dataclass
from .stimulus import Stimulus
from typing import Optional

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
