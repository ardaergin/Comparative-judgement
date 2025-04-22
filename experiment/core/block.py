from dataclasses import dataclass
from typing import List, Optional
from psychopy import visual, core, event
from .trial import Trial
from ..managers import DataManager

@dataclass
class BlockConfig:
    """Configuration settings for a block of trials"""
    skip_time_limit: float = 4.0
    prompt_text: str = "Which is more similar to the reference image?"
    num_breaks: int = 0
    break_wait_time: int = 20
    font: str = "Times New Roman"
    left_text: str = "Left Image"
    right_text: str = "Right Image"
    reference_text: str = "Reference Image"
    text_height: int = 0.03
    referant_present: bool = False

class Block:
    """Manages a block of trials with consistent configuration and presentation"""
    
    def __init__(
        self,
        window: visual.Window,
        trials: List[Trial],
        config: Optional[BlockConfig] = None,
        data_manager: Optional[DataManager]=None
    ):
        self.window = window
        self.trials = trials
        self.config = config or BlockConfig()
        self.data_manager = data_manager
        self.clock = core.Clock()

        # Initialize block-level properties
        self.n_trials = len(trials)
        self.n_blocks = self.config.num_breaks + 1
        self.block_size = self.n_trials // self.n_blocks if self.n_blocks > 1 else self.n_trials
        
        # Initialize static stimuli
        self._init_static_stimuli()

    def _init_static_stimuli(self):
        """Initialize static visual elements used across trials"""
        self.fixation = visual.TextStim(
            self.window, 
            text="+", 
            height=0.08, 
            color='black',
            font=self.config.font,
            pos=(0, 0)
        )
        
        self.missed_message = visual.TextStim(
            self.window,
            text=("You missed the last trial.\nPlease respond faster.\n\n"
                  "We are interested in your initial impressions.\n\n"
                  "As a reminder: left = D, right = K\n\n"
                  "Press the SPACE BAR to continue."),
            color='black',
            font=self.config.font,
            height=self.config.text_height,
            wrapWidth=1,
            pos=(0, 0)
        )
        
        self.prompt = visual.TextStim(
            self.window,
            text=self.config.prompt_text,
            color='black',
            font=self.config.font,
            height=self.config.text_height,
            wrapWidth=5, # very large so it does not wrap.
            pos=(0, 0.40)
        )

    def _get_image_positions(self, round_type: str) -> dict:
        """Get positions for images and labels based on round type in normalized units"""
        
        if self.config.referant_present:
            if round_type == "liking" or round_type == "similarity":
                return {
                    # Comparison positions:
                    'left_image': (-0.3, -0.30),
                    'left_text': (-0.3, -0.15),

                    'right_image': (0.3, -0.30),
                    'right_text': (0.3, -0.15),

                    # Reference positions:
                    'reference_text': (0, 0.30),
                    'reference_image': (0, 0.15)
                }
            else: # if round_type == "pracice":
                return {
                    # Comparison positions:
                    'left_image': (-0.3, -0.20),
                    'left_text': (-0.3, -0.00),

                    'right_image': (0.3, -0.20),
                    'right_text': (0.3, -0.00),

                    # Reference positions:
                    'reference_text': (0, 0.30),
                    'reference_image': (0, 0.10)
                }
        else: # (if referent not present)
            return {
                # Comparison positions:
                'left_text': (-0.3, 0.15),
                'left_image': (-0.3, -0.05),

                'right_text': (0.3, 0.15),
                'right_image': (0.3, -0.05)
            }

    def _create_text_stimuli(self, positions: dict, round_type: str) -> dict:
        """Create text stimuli for image labels"""
        text_stimuli = {
            'left': visual.TextStim(
                self.window,
                text=self.config.left_text,
                color='black',
                font=self.config.font,
                height=self.config.text_height,
                pos=positions['left_text']
            ),
            'right': visual.TextStim(
                self.window,
                text=self.config.right_text,
                color='black',
                font=self.config.font,
                height=self.config.text_height,
                pos=positions['right_text']
            )
        }
        
        if self.config.referant_present:
            text_stimuli['reference'] = visual.TextStim(
                self.window,
                text=self.config.reference_text,
                color='black',
                font=self.config.font,
                height=self.config.text_height,
                pos=positions['reference_text']
            )
            
        return text_stimuli

    def _show_feedback(self, chosen_stim: visual.ImageStim, trial: Trial):
        """Display feedback for chosen stimulus"""
        ## If just want to display the chosen image for feedback:
        # chosen_stim.psychopy_stim.draw()
        # self.window.flip()
        # core.wait(0.5)

        blue_border = visual.Rect(
            self.window,
            width=chosen_stim.psychopy_stim.size[0] + 0.05,
            height=chosen_stim.psychopy_stim.size[1] + 0.05,
            lineColor='blue',
            lineWidth=5,
            pos=chosen_stim.psychopy_stim.pos
        )

        self.prompt.draw()
        if self.config.referant_present:
            trial.reference.psychopy_stim.draw()
        trial.pair.left_stimuli.psychopy_stim.draw()
        trial.pair.right_stimuli.psychopy_stim.draw()
        blue_border.draw()

        self.window.flip()
        core.wait(0.5)

    def _show_break_screen(self, current_block: int):
        """Display break screen between blocks with a countdown timer"""
        remaining_time = self.config.break_wait_time
        
        # Create the basic break text
        break_text = visual.TextStim(
            self.window,
            text="",  # Will be updated each second
            color='black',
            font=self.config.font,
            height=self.config.text_height,
            wrapWidth=1,
            pos=(0, 0)
        )
        
        # Create countdown text
        countdown_text = visual.TextStim(
            self.window,
            text="",  # Will be updated each second
            color='black',
            font=self.config.font,
            height=self.config.text_height * 1.5,  # Slightly larger for visibility
            pos=(0, -0.2)  # Position below the break text
        )
        
        # Start countdown
        timer = core.CountdownTimer(self.config.break_wait_time)
        
        while remaining_time > 0:
            # Update remaining time
            remaining_time = int(timer.getTime())
            
            # Update break text
            break_text.text = (
                f"Block {current_block} of {self.n_blocks} completed.\n\n"
                f"Please take a short break.\n"
                "You will be able to continue after 20 seconds."
            )
            
            # Update countdown text
            if remaining_time > 0:
                countdown_text.text = f"{remaining_time}"
            
            # Draw both text stimuli
            break_text.draw()
            countdown_text.draw()
            self.window.flip()
            
            # Check for escape key
            if event.getKeys(keyList=['escape']):
                core.quit()
                
            # Brief pause to prevent excessive CPU usage
            core.wait(0.1)
        
        # Show continue message
        break_text.text = (
            f"Block {current_block} of {self.n_blocks} completed.\n\n"
            "You can now continue.\n"
            "Press SPACE when you are ready."
        )
        countdown_text.text = ""  # Clear the countdown
        
        break_text.draw()
        countdown_text.draw()
        self.window.flip()
        
        # Wait for space key
        event.waitKeys(keyList=['space'])

    def _handle_response(self, trial: Trial, keys) -> bool:
        """Process response for a trial. Returns False if experiment should end."""
        if not keys:
            self.missed_message.draw()
            self.window.flip()
            event.waitKeys(keyList=['space'])
            trial.response = "missed"
            return True

        key, rt = keys[0]
        if key == 'escape':
            return False
            
        trial.response = key
        trial.reaction_time = rt
        
        # Determine chosen stimulus for feedback
        chosen_stim = (trial.pair.left_stimuli if key == 'd' 
                      else trial.pair.right_stimuli)
        self._show_feedback(chosen_stim, trial)
        return True

    def run(self) -> List[Trial]:
        """Run all trials in the block and return completed trials"""
        for trial_num, trial in enumerate(self.trials, 1):
            # Show fixation
            self.fixation.draw()
            self.window.flip()
            core.wait(0.5)

            # Set up positions
            positions = self._get_image_positions(trial.round_type)
            trial.pair.left_stimuli.set_position(positions['left_image'])
            trial.pair.right_stimuli.set_position(positions['right_image'])
            
            # Create and position text stimuli
            text_stimuli = self._create_text_stimuli(positions, trial.round_type)

            # Draw trial
            self.prompt.draw()
            if trial.reference and self.config.referant_present:
                trial.reference.set_position(positions['reference_image'])
                trial.reference.psychopy_stim.draw()
                text_stimuli['reference'].draw()
            trial.pair.left_stimuli.psychopy_stim.draw()
            trial.pair.right_stimuli.psychopy_stim.draw()
            text_stimuli['left'].draw()
            text_stimuli['right'].draw()
            self.window.flip()

            # Collect response
            self.clock.reset()
            keys = event.waitKeys(
                keyList=['d', 'k', 'escape'],
                timeStamped=self.clock,
                maxWait=self.config.skip_time_limit
            )

            # Handle response
            if not self._handle_response(trial, keys):
                break

            # After handling the trial response, immediately save the trial.
            if self.data_manager is not None:
                self.data_manager.save_trial(trial)

            # Show break screen if needed
            if (self.n_blocks > 1 and 
                trial_num % self.block_size == 0 and 
                trial_num < self.n_trials and 
                trial_num // self.block_size < self.n_blocks):
                self._show_break_screen(trial_num // self.block_size)

        return self.trials
