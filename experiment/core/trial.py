from dataclasses import dataclass
from typing import Optional, List
from .comparison import Comparison
from .stimulus import Stimulus

@dataclass
class Trial:
    """Represents a single trial"""
    trial_num: int
    pair: Comparison
    round_type: str  # "practice", "similarity", or "liking"
    reference: Optional[Stimulus] = None
    response: Optional[str] = None
    reaction_time: Optional[float] = None
    
    def to_csv_row(self, participant_id) -> List[str]:
        """Convert trial data to CSV row format"""
        return [
            participant_id,
            str(self.trial_num),
            self.round_type,
            self.pair.left_stimuli.filename,
            self.pair.right_stimuli.filename,
            str(self.response) if self.response else "missed",
            str(self.reaction_time) if self.reaction_time else "NA"
        ]
