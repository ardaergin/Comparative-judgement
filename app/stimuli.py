from psychopy import visual
import os
import itertools
import random

def load_stimuli(comparison_dir):
    """
    Load image filenames from the specified directory.

    Parameters:
        comparison_dir: Path to the directory containing comparison images.

    Returns:
        A list of image filenames in the directory.
    """
    # Get all comparison images
    comparison_files = [
        f for f in os.listdir(comparison_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    # Ensure at least two images
    if len(comparison_files) < 2:
        raise ValueError("Not enough comparison images found. At least two are required.")
    
    return comparison_files

def preload_images(win, image_folder, image_list, size):
    """
    Preload images into memory to reduce delays during the experiment.

    Parameters:
        win: PsychoPy window object.
        image_folder: Path to the folder containing images.
        image_list: List of image filenames.

    Returns:
        A dictionary where keys are image filenames and values are preloaded ImageStim objects.
    """
    preloaded_images = {}
    for image_name in image_list:
        image_path = os.path.join(image_folder, image_name)
        preloaded_images[image_name] = visual.ImageStim(win, image=image_path, size=size)
    return preloaded_images

def setup_stimuli(comparison_files, pair_repeats):
    """
    Set up trials by creating a randomized list of image pairs.

    Parameters:
        comparison_files: List of image filenames.
        pair_repeats: Number of times to repeat each unique pair.

    Returns:
        A randomized list of image pairs.
    """
    # Generate all unique pairs
    all_pairs = list(itertools.combinations(comparison_files, 2))
    trial_list = all_pairs * pair_repeats
    random.shuffle(trial_list)
    return trial_list
