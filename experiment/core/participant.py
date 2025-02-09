from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
from .trial import Trial

@dataclass
class Participant:
    """Manages all experimental data for a participant"""
    participant_id: str
    trials: List[Trial] = field(default_factory=list)
    demographics: Dict = field(default_factory=dict)
    feedback: str = ""
    start_time: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S")) # to initalize/write after ID is taken
    end_time: str = None # TODO: to inilize/write at the last screen
    
    def _get_datafile_name(self) -> str:
        """Ensure the filename is correctly formatted as a string"""
        return str(f"{self.participant_id}_{self.start_time}")

    def add_trial(self, trial: Trial):
        self.trials.append(trial)
    
    def add_demographics(self, demographics: Dict):
        self.demographics = demographics
    
    def mark_end(self):
        """Record the end time of the experiment."""
        self.end_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    def add_feedback(self, feedback: str):
        self.feedback = feedback
    
    def to_json(self) -> Dict:
        """Convert all data to JSON-serializable format"""
        return {
            "participant_id": self.participant_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "demographics": self.demographics,
            "feedback": self.feedback,
            "trials": [
                {
                    "trial_num": trial.trial_num,
                    "round_type": trial.round_type,
                    "left_stimulus": trial.pair.left_stimuli.filename,
                    "right_stimulus": trial.pair.right_stimuli.filename,
                    "comparison_hash": hash(trial.pair),
                    "comparison_order": trial.pair.order_indicator,
                    "response": trial.response,
                    "reaction_time": trial.reaction_time
                }
                for trial in self.trials
            ]
        }
