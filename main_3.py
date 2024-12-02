import numpy as np
import pandas as pd
from psychopy import visual, core, event, gui
import random
import os

class AdaptiveComparativeJudgementExperiment:
    def __init__(self, num_trials=50, initial_quality=0.0, alpha=0.05):
        """
        Initialize the ACJ experiment.

        :param num_trials: Total number of trials.
        :param initial_quality: Initial quality parameter for each item.
        :param alpha: Learning rate for updating item scores.
        """
        # Experiment setup
        self.num_trials = num_trials
        self.alpha = alpha
        self.quality_params = {}  # Store quality parameters for items
        self.win_counts = {}      # Track wins for items
        self.comparisons = set()  # Keep track of all comparisons made

        # Initialize PsychoPy window
        self.win = visual.Window(size=[1200, 800], color="gray", units="norm")

        # Prepare GUI for participant info
        self.participant_info = self.get_participant_info()

        # Load images
        self.comp_folder = "data/images/comparison"
        self.ref_folder = "data/images/reference"
        self.ref_image = "ref_image.png"

        self.images = self.load_images()
        for image in self.images:
            self.quality_params[image] = initial_quality
            self.win_counts[image] = 0

        # Result storage
        self.results = {
            "trial": [],
            "reference": [],
            "left": [],
            "right": [],
            "chosen": [],
            "quality_params": [],
        }

    def load_images(self):
        """
        Load image file names from the specified folder.
        """
        return [f for f in os.listdir(self.comp_folder)]
    
    def get_participant_info(self):
        """
        Collect participant information via GUI.
        """
        participant_info = {"Participant ID": "", "Age": "", "Gender": ["Male", "Female", "Other"]}
        dlg = gui.DlgFromDict(dictionary=participant_info, title="Participant Information")
        if not dlg.OK:
            core.quit()
        return participant_info

    def select_pair(self):
        """
        Adaptive pair selection based on quality parameters.
        """
        # Exclude pairs already compared
        possible_pairs = [(i, j) for i in self.images for j in self.images if i != j and (i, j) not in self.comparisons]
        if not possible_pairs:
            return None, None

        # Select the pair with the closest quality parameters
        pair = min(possible_pairs, key=lambda x: abs(self.quality_params[x[0]] - self.quality_params[x[1]]))
        return pair

    def update_quality_params(self, winner, loser):
        """
        Update quality parameters based on comparison results.
        """
        delta = self.quality_params[winner] - self.quality_params[loser]
        prob_winner = 1 / (1 + np.exp(-delta))

        # Update using Bradley-Terry model
        self.quality_params[winner] += self.alpha * (1 - prob_winner)
        self.quality_params[loser] -= self.alpha * (1 - prob_winner)

    def run_experiment(self):
        """
        Main experiment loop.
        """
        instruction_text = visual.TextStim(
            self.win, text="Choose the image most similar to the reference.", pos=(0, 0.8), height=0.1
        )

        for trial in range(self.num_trials):
            reference_image = self.ref_image # or `random.choice(self.images)`
            left, right = self.select_pair()
            if not left or not right:
                break  # No more pairs to compare

            # Track comparison
            self.comparisons.add((left, right))

            # Display stimuli
            reference_stim = visual.ImageStim(self.win, image=os.path.join(self.ref_folder, reference_image), pos=(0, 0.3), size=(0.5, 0.5))
            left_stim = visual.ImageStim(self.win, image=os.path.join(self.comp_folder, left), pos=(-0.5, -0.3), size=(0.3, 0.3))
            right_stim = visual.ImageStim(self.win, image=os.path.join(self.comp_folder, right), pos=(0.5, -0.3), size=(0.3, 0.3))

            instruction_text.draw()
            reference_stim.draw()
            left_stim.draw()
            right_stim.draw()
            self.win.flip()

            # Wait for participant response
            keys = event.waitKeys(keyList=["left", "right", "escape"])
            if "escape" in keys:
                break

            chosen = left if "left" in keys else right
            not_chosen = right if chosen == left else left

            # Update results
            self.results["trial"].append(trial)
            self.results["reference"].append(reference_image)
            self.results["left"].append(left)
            self.results["right"].append(right)
            self.results["chosen"].append(chosen)
            self.results["quality_params"].append(self.quality_params.copy())

            # Update quality parameters
            self.update_quality_params(chosen, not_chosen)

        # Save results
        self.save_results()
        self.win.close()
        core.quit()

    def save_results(self):
        """
        Save results to a CSV file.
        """
        results_df = pd.DataFrame(self.results)
        filename = f"data/responses/acj_results_{self.participant_info['Participant ID']}.csv"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        results_df.to_csv(filename, index=False)
        print(f"Results saved to {filename}")


def main():
    experiment = AdaptiveComparativeJudgementExperiment()
    experiment.run_experiment()


if __name__ == "__main__":
    main()
