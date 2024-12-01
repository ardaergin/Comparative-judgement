import numpy as np
import pandas as pd
from psychopy import visual, core, event, gui, data
import random

class AdaptiveComparativeJudgementExperiment:
    def __init__(self, num_trials=50, initial_difficulty=0.5):
        """
        Initialize the experiment parameters
        
        :param num_trials: Total number of trials in the experiment
        :param initial_difficulty: Starting point for stimulus selection
        """
        # Setup experiment window
        self.win = visual.Window(size=[1200, 800], color='gray', units='norm')
        
        # Prepare GUI for participant info
        self.participant_info = self.get_participant_info()
        
        # Stimulus presentation parameters
        self.reference_stim = None
        self.left_stim = None
        self.right_stim = None
        
        # Adaptive algorithm parameters
        self.num_trials = num_trials
        self.difficulty = initial_difficulty
        
        # Results storage
        self.results = {
            'trial': [],
            'reference_image': [],
            'left_image': [],
            'right_image': [],
            'chosen_image': [],
            'difficulty': []
        }
        
        # Prepare stimuli placeholders
        # In a real experiment, replace these with actual image paths or generation method
        self.image_pool = self._generate_image_pool()
    
    def get_participant_info(self):
        """
        Collect participant information via GUI
        """
        participant_info = {
            'Participant ID': '',
            'Age': '',
            'Gender': ['Male', 'Female', 'Other']
        }
        
        dlg = gui.DlgFromDict(dictionary=participant_info, title='Participant Information')
        
        if not dlg.OK:
            core.quit()
        
        return participant_info
    
    def _generate_image_pool(self, pool_size=100):
        """
        Generate a pool of synthetic images for demonstration
        In a real experiment, replace with actual image loading
        
        :param pool_size: Number of synthetic images to generate
        :return: List of image representations
        """
        # This is a placeholder. Replace with actual image loading or generation
        return [np.random.rand(100, 100) for _ in range(pool_size)]
    
    def select_stimuli(self):
        """
        Adaptive stimulus selection based on current difficulty
        
        :return: Tuple of (reference_image, left_image, right_image)
        """
        # Use difficulty to guide image selection
        # This is a simplistic implementation - customize based on your specific needs
        reference = random.choice(self.image_pool)
        
        # Select images with varying degrees of similarity based on difficulty
        candidates = [img for img in self.image_pool if img is not reference]
        left = random.choice(candidates)
        right = random.choice([img for img in candidates if img is not left])
        
        return reference, left, right
    
    def update_difficulty(self, chosen_image, reference, left, right):
        """
        Update difficulty based on participant's choice
        
        :param chosen_image: The image selected by participant
        :param reference: Reference image
        :param left: Left image
        :param right: Right image
        """
        # Simple difficulty adjustment logic
        # In a real study, use more sophisticated psychometric methods
        if chosen_image is reference:
            self.difficulty += 0.05
        else:
            self.difficulty -= 0.05
        
        # Constrain difficulty between 0 and 1
        self.difficulty = max(0, min(1, self.difficulty))
    
    def run_experiment(self):
        """
        Main experiment procedure
        """
        # Prepare text stimuli
        instruction_text = visual.TextStim(
            self.win, 
            text='Choose the image most similar to the reference image',
            pos=(0, 0.8), 
            height=0.1
        )
        
        for trial in range(self.num_trials):
            # Select stimuli for this trial
            reference, left, right = self.select_stimuli()
            
            # Create visual stimuli
            reference_stim = visual.ImageStim(
                self.win, image=reference, pos=(0, 0.3), size=(0.5, 0.5)
            )
            left_stim = visual.ImageStim(
                self.win, image=left, pos=(-0.5, -0.3), size=(0.3, 0.3)
            )
            right_stim = visual.ImageStim(
                self.win, image=right, pos=(0.5, -0.3), size=(0.3, 0.3)
            )
            
            # Draw stimuli
            instruction_text.draw()
            reference_stim.draw()
            left_stim.draw()
            right_stim.draw()
            
            self.win.flip()
            
            # Wait for participant response
            keys = event.waitKeys(keyList=['left', 'right', 'escape'])
            
            if 'escape' in keys:
                break
            
            # Determine chosen image
            chosen_image = left if 'left' in keys else right
            
            # Store trial results
            self.results['trial'].append(trial)
            self.results['reference_image'].append(reference)
            self.results['left_image'].append(left)
            self.results['right_image'].append(right)
            self.results['chosen_image'].append(chosen_image)
            self.results['difficulty'].append(self.difficulty)
            
            # Update difficulty
            self.update_difficulty(chosen_image, reference, left, right)
        
        # Save results
        self.save_results()
        
        # Cleanup
        self.win.close()
        core.quit()
    
    def save_results(self):
        """
        Save experiment results to a CSV file
        """
        results_df = pd.DataFrame(self.results)
        filename = f"adaptive_judgement_{self.participant_info['Participant ID']}.csv"
        results_df.to_csv(filename, index=False)
        print(f"Results saved to {filename}")

def main():
    experiment = AdaptiveComparativeJudgementExperiment()
    experiment.run_experiment()

if __name__ == "__main__":
    main()
