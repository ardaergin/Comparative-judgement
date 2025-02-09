from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
from psychopy import visual, core, event
import random
import os
import itertools
import os
from ..core import Stimulus, Comparison, Trial

class StimuliManager:
    """Manages stimuli loading and trial generation"""
    def __init__(self, comparison_dir: str, reference_dir: Optional[str] = None):
        """
        Args:
            comparison_dir: Directory containing comparison images.
            reference_dir: Directory containing a single reference image.
        """
        self.comparison_dir = comparison_dir # path to the folder with multiple images
        self.reference_dir = reference_dir  # path to the folder with a single image
        self.stimuli: List[Stimulus] = []
        self.reference: Optional[Stimulus] = None
        self.pairs: List[Comparison] = []
        
    def load_stimuli(self, win: visual.Window):
        """
        Load and preload all stimuli.

        Creates a Stimulus instance for each image in the comparison directory.
        Also loads a reference stimulus from the reference directory (if provided).
        """

        # Load comparison stimuli
        comp_files = [f for f in os.listdir(self.comparison_dir)
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for filename in comp_files:
            image_path = os.path.join(self.comparison_dir, filename)
            stimulus = Stimulus(
                filename=filename,
                image_path=image_path,
                win=win
            )
            self.stimuli.append(stimulus)
        
        # Load reference stimulus from reference directory if provided
        if self.reference_dir:
            if not os.path.isdir(self.reference_dir):
                raise ValueError(f"Provided reference path {self.reference_dir} is not a directory.")
            
            # List all image files in the reference directory
            ref_files = [f for f in os.listdir(self.reference_dir)
                         if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            if not ref_files:
                raise ValueError("No image files found in the reference directory.")
            
            # Select the first (and only) image in the list
            ref_filename = ref_files[0]
            ref_image_path = os.path.join(self.reference_dir, ref_filename)
            
            self.reference = Stimulus(
                filename=ref_filename,
                image_path=ref_image_path,
                win=win
            )

    def generate_trials(self, round_type: str, pair_repeats: int = 1) -> List[Trial]:
        """Generate trials with consistent left-right positioning"""
        if not self.pairs:  # Only generate pairs if not already generated
            # Generate all unique pairs
            all_pairs = list(itertools.combinations(self.stimuli, 2))
            
            # Randomly decide left-right positioning for each pair
            self.pairs = [
                Comparison(left_stimuli=pair[0], right_stimuli=pair[1])
                if random.choice([True, False]) else
                Comparison(left_stimuli=pair[1], right_stimuli=pair[0])
                for pair in all_pairs
            ]
        
        # Create trials with the same pairs but in random order
        trials = []
        trial_num = 1
        for _ in range(pair_repeats):
            shuffled_pairs = random.sample(self.pairs, len(self.pairs))
            for pair in shuffled_pairs:
                trials.append(Trial(
                    trial_num=trial_num,
                    pair=pair,
                    round_type=round_type,
                    reference=self.reference if round_type != "liking" else None
                ))
                trial_num += 1
        
        return trials
