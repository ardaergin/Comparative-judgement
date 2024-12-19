import os
import itertools
import random

def load_stimuli(comparison_dir):
    # Get all comparison images
    comparison_files = [
        f for f in os.listdir(comparison_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    # Ensure at least two images
    if len(comparison_files) < 2:
        raise ValueError("Not enough comparison images found. At least two are required.")
    
    return comparison_files

def setup_stimuli(comparison_files, pair_repeats):
    # Generate all unique pairs
    all_pairs = list(itertools.combinations(comparison_files, 2))
    trial_list = all_pairs * pair_repeats
    random.shuffle(trial_list)
    return trial_list
