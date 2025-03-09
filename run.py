from psychopy import visual, core
from experiment import DataManager, StimuliManager
from experiment import BlockConfig, Block, Participant
from experiment import Display
from experiment import ask_id, ask_age, ask_diet, ask_eat_frequency, ask_gender, ask_nationality, ask_feedback


class ExperimentRunner:
    """Main experiment runner class"""
    
    def __init__(self):
        # Experiment parameters
        self.pair_repeats = 1
        self.skip_time_limit = 4
        self.experiment_font = "Times New Roman"
        
        # Set up window
        self.display = Display(visual.Window(
            fullscr=True,
            color=[1, 1, 1],
            units='height'
        ), font=self.experiment_font)
        
        # Initialize screens
        self.screens = {}
        self._init_screens()

        # Load all stimuli
        self._load_stimuli()

    def _init_screens(self):
        """Preload all screen objects."""

        self.screens["experiment_info"] = self.display.load_image("texts/0_experiment_info.png")
        self.screens["consent"] = self.display.load_text_from_file("texts/1_informed_consent.txt")

        self.screens["pre_instructions"] = self.display.load_text_from_file("texts/3_pre_instructions.txt")
        self.screens["practice_instructions"] = self.display.load_image("texts/4_practice_instructions.png")
        self.screens["practice_aftermath"] = self.display.load_text_from_file("texts/4_practice_aftermath.txt")

        self.screens["similarity_instructions"] = self.display.load_image("texts/5_trial_instructions_sim.png")
        self.screens["similarity_instructions_visual"] = self.display.load_image("texts/5_trial_instructions_sim_visual.png")

        self.screens["liking_instructions"] = self.display.load_image("texts/6_trial_instructions_liking.png")
        self.screens["liking_instructions_visual"] = self.display.load_image("texts/6_trial_instructions_liking_visual.png")

        self.screens["pre_demographics"] = self.display.load_text_from_file("texts/7_pre_demographics.txt")
                
        self.screens["end_of_experiment"] = self.display.load_text_from_file("texts/9_end_of_experiment.txt")

    def _load_stimuli(self):
        """Load all stimuli for practice and main trials"""
        # Practice stimuli
        self.practice_stimuli_manager = StimuliManager(
            comparison_dir='images/practice/comparison',
            reference_dir='images/practice/reference'
        )
        self.practice_stimuli_manager.load_stimuli(self.display.window)
        
        # Main stimuli
        self.trial_stimuli_manager = StimuliManager(
            comparison_dir='images/trials/comparison',
            reference_dir='images/trials/reference'
        )
        self.trial_stimuli_manager.load_stimuli(self.display.window)

    def run(self):
        """Run the complete experiment"""
        try:        
            # Load all stimuli
            self._load_stimuli()
    
            # Starting the experiment
            self.display.display_stimulus(self.screens["experiment_info"])
            self.display.display_stimulus(self.screens["consent"], allow_escape=True)
            
            # Initialize Participant instance and Data manager
            participant_id = ask_id(self.display)
            participant = Participant(participant_id)
            data_manager = DataManager(participant)
            
            # Show pre-instructions
            self.display.display_stimulus(self.screens["pre_instructions"])
            
            # -------------------------
            # PRACTICE BLOCK
            # -------------------------
            # Prepare the practice block
            practice_trials = self.practice_stimuli_manager.generate_trials(
                round_type="practice", 
                pair_repeats=self.pair_repeats)
            
            practice_config = BlockConfig(
                prompt_text="Which of the two citrus fruits is MORE SIMILAR to a prototypical ORANGE?",
                num_breaks=0,
                left_text="Citrus fruit A",
                right_text="Citrus fruit B",
                reference_text="Orange"
            )
            practice_block = Block(
                self.display.window,
                trials=practice_trials, 
                config=practice_config,
                data_manager=data_manager)
            
            # Display practice instructions
            self.display.display_stimulus(self.screens["practice_instructions"])
            
            # Run practice block
            practice_block.run()
            
            # Show aftermath of practice
            self.display.display_stimulus(self.screens["practice_aftermath"])

            # -------------------------
            # SIMILARITY BLOCK
            # -------------------------
            # Prepare the similarity block
            similarity_trials = self.trial_stimuli_manager.generate_trials(
                round_type="experimental_trial", 
                pair_repeats=self.pair_repeats)
            for trial in similarity_trials:
                print(trial.pair.left_stimuli.filename, trial.pair.right_stimuli.filename)

            similarity_config = BlockConfig(
                prompt_text="Which of the two plant-based steaks is MORE SIMILAR to a prototypical BEEF STEAK?",
                num_breaks=2,
                break_wait_time=20,
                left_text="PLANT-BASED STEAK A",
                right_text="PLANT-BASED STEAK B",
                reference_text="BEEF STEAK"
            )
            similarity_block = Block(
                self.display.window, 
                trials=similarity_trials, 
                config=similarity_config,
                data_manager=data_manager)
            
            # Display similarity instructions (you can choose to show one or both screens)
            self.display.display_stimulus(self.screens["similarity_instructions"])
            self.display.display_stimulus(self.screens["similarity_instructions_visual"])
            
            # Run similarity block
            similarity_block.run()
            
            # -------------------------
            # LIKING BLOCK
            # -------------------------
            # Generate liking trials (for liking, you might not include a reference image)
            liking_trials = self.trial_stimuli_manager.generate_trials(
                round_type="experimental_trial", 
                pair_repeats=self.pair_repeats)
            for trial in liking_trials:
                print(trial.pair.left_stimuli.filename, trial.pair.right_stimuli.filename)

            liking_config = BlockConfig(
                prompt_text="Which of the two plant-based steaks do you LIKE MORE?",
                num_breaks=2,
                break_wait_time=20,
                left_text="PLANT-BASED STEAK A",
                right_text="PLANT-BASED STEAK B",
            )
            liking_block = Block(
                self.display.window, 
                trials=liking_trials, 
                config=liking_config,
                data_manager=data_manager)
            
            # Display liking instructions
            self.display.display_stimulus(self.screens["liking_instructions"])
            self.display.display_stimulus(self.screens["liking_instructions_visual"])
            
            # Run liking block
            liking_block.run()

            # -------------------------
            # DEMOGRAPHICS AND FEEDBACK
            # -------------------------
            self.display.display_stimulus(self.screens["pre_demographics"])

            # Demographics
            demographics = {}
            demographics['gender'] = ask_gender(self.display)
            demographics['age'] = ask_age(self.display)
            demographics['nationality'] = ask_nationality(self.display)
            demographics['diet'] = ask_diet(self.display)
            demographics['eat_frequency'] = ask_eat_frequency(self.display)
            data_manager.save_demographics(demographics)

            # Recording the end time
            participant.mark_end()

            # Feedback
            feedback = ask_feedback(self.display)
            data_manager.save_feedback(feedback)

            # Save all data
            data_manager.save_all()

            # End of experiment screen
            self.display.display_stimulus(self.screens["end_of_experiment"], wait_for_space=False, show_continue=False)
            core.wait(30)
            self.display.quit_experiment()

        except Exception as e:
            print("An error occurred:", e)
            self.display.quit_experiment()

if __name__ == '__main__':
    runner = ExperimentRunner()
    runner.run()
