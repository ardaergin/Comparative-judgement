from typing import Optional, List, Dict, Tuple
from psychopy import visual, core, event
import csv
import os
import os
import json
from ..core import Participant, Trial

class DataManager:
    """Manages data saving operations"""
    def __init__(self, participant_id: str):
        self.participant = Participant(participant_id)
        self.ensure_data_dir()
    
    @staticmethod
    def ensure_data_dir():
        """Ensure data directory exists"""
        if not os.path.exists('data'):
            os.makedirs('data')
    
    def save_trial(self, trial: Trial):
        """Save trial data to CSV and update experiment data"""
        self.participant.add_trial(trial)
        
        # Get unique file name with ID + timestamp
        file_name = self.participant._get_datafile_name() 
        # Append to CSV
        csv_path = f"data/{file_name}.csv"
        write_header = not os.path.exists(csv_path)
        
        with open(csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(['trial', 'round_type', 'left_image', 'right_image', 'response', 'rt'])
            writer.writerow(trial.to_csv_row())
    
    def save_demographics(self, demographics: Dict):
        """Save demographics to experiment data"""
        self.participant.add_demographics(demographics)
    
    def save_feedback(self, feedback: str):
        """Save feedback to experiment data"""
        self.participant.add_feedback(feedback)
    
    def save_all(self):
        """Save all experiment data to JSON"""
        file_name = self.participant._get_datafile_name()
        json_path = f"data/{file_name}.json"
        with open(json_path, 'w') as f:
            json.dump(self.participant.to_json(), f, indent=2)
