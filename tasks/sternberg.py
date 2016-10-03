import os
import sys
import random
import time
import pandas as pd
import pygame

from pygame.locals import *
from itertools import product
from utils import display


class Sternberg(object):
    def __init__(self, screen, background, blocks=2):
        # Get the pygame display window
        self.screen = screen
        self.background = background

        # Set fonts and font sizes
        self.font = pygame.font.SysFont("arial", 30)
        self.stim_font = pygame.font.SysFont("arial", 50)

        # Get screen info
        self.screen_x = self.screen.get_width()
        self.screen_y = self.screen.get_height()

        # Fill background
        self.background.fill((255, 255, 255))
        pygame.display.set_caption("Sternberg Task")
        pygame.mouse.set_visible(0)

        # Load images
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.image_path = os.path.join(self.base_dir, "images", "Sternberg")

        self.img_left = pygame.image.load(
            os.path.join(self.image_path, 'left_arrow.png'))

        self.img_right = pygame.image.load(
            os.path.join(self.image_path, 'right_arrow.png'))

        # Experiment options
        # Timings are taken from Sternberg (1966)
        # Block sizes are taken from Martins (2012)
        self.num_blocks = blocks
        self.stim_duration = 1200
        self.between_stim_duration = 250
        self.probe_warn_duration = 2000
        self.probe_duration = 2250  # Max time per probe, from Martins (2012)
        self.feedback_duration = 1000
        self.ITI = 1500

        self.stim_set = range(10)
        self.set_size = (2, 6)
        self.probe_type = ("present", "absent")

        # Create condition combinations
        self.combinations = list(product(self.set_size, self.probe_type))

        # Create practice trials
        # This gives 24 practice trials
        self.practice_combinations = self.combinations * 6
        random.shuffle(self.practice_combinations)
        self.practice_trials = self.create_trials(self.practice_combinations)

        # Create main trial blocks
        self.blocks = []  # List will contain a dataframe for each block

        for i in range(self.num_blocks):
            # This creates 48 trials per block
            block_combinations = self.combinations * 12
            random.shuffle(block_combinations)

            block = self.create_trials(block_combinations)
            block['block'] = str(i+1)  # Store the block number
            self.blocks.append(block)

    def create_trials(self, combinations):
        df = pd.DataFrame(combinations, columns=("setSize", "probeType"))

        for i, r in df.iterrows():
            # Store the current used set
            used_set = random.sample(self.stim_set, r['setSize'])
            unused_set = list(set(self.stim_set) - set(used_set))

            df.set_value(i, 'set', ''.join(str(x) for x in used_set))

            # Store the target probe number
            # Probe will be from/in the set 50% of the time (probe present)
            if r['probeType'] == "present":
                df.set_value(i, 'probe', str(random.choice(used_set)))
            else:
                df.set_value(i, 'probe', str(random.choice(unused_set)))

            # Store blank columns to be used later
            df['trialNum'] = ''
            df['block'] = ''
            df['response'] = ''
            df['RT'] = ''
            df['correct'] = ''

            # Rearrange the dataframe
            columns = ['trialNum', 'block', 'setSize', 'probeType', 'set',
                       'probe', 'response', 'RT', 'correct']
            df = df[columns]

        return df

    def display_trial(self, df, i, r, trial_type):
        # Clear screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        # Display number sequence
        self.display_sequence(r['set'])

        # Display probe warning
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.stim_font, "+", "center", "center")
        pygame.display.flip()

        display.wait(self.probe_warn_duration)

        # Display blank screen
        display.blank_screen(self.screen, self.background,
                             self.between_stim_duration)

        # Display probe
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.stim_font, r['probe'],
                     "center", "center", (0, 0, 255))

        # Display key reminders if practice trials
        if trial_type == "practice":
            display.image(self.screen, self.img_left,
                          450 - self.img_left.get_rect().width/2,
                          self.screen_y/2 + 150)
            yes_text = self.font.render("(yes)", 1, (0, 0, 0))
            display.text(self.screen, self.font, yes_text,
                         450 - yes_text.get_rect().width/2,
                         self.screen_y/2 + 160)

            display.image(self.screen, self.img_right,
                          self.screen_x-450-self.img_right.get_rect().width/2,
                          self.screen_y/2 + 150)
            no_text = self.font.render("(no)", 1, (0, 0, 0))
            display.text(self.screen, self.font, no_text,
                         self.screen_x - 450 - no_text.get_rect().width/2,
                         self.screen_y/2 + 160)

        pygame.display.flip()

        start_time = int(round(time.time() * 1000))

        # Clear the event queue before checking for responses
        pygame.event.clear()
        wait_response = True
        while wait_response:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_LEFT:
                    df.set_value(i, "response", "present")
                    wait_response = False
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    df.set_value(i, "response", "absent")
                    wait_response = False
                elif event.type == KEYDOWN and event.key == K_F12:
                    sys.exit(0)

            end_time = int(round(time.time() * 1000))

            # If time limit has been reached, consider it a missed trial
            if end_time - start_time >= self.probe_duration:
                wait_response = False

        # Store RT
        rt = int(round(time.time() * 1000)) - start_time
        df.set_value(i, "RT", rt)

        # Display blank screen
        display.blank_screen(self.screen, self.background,
                             self.between_stim_duration)

        # Display feedback
        self.screen.blit(self.background, (0, 0))

        if df["probeType"][i] == df["response"][i]:
            df.set_value(i, "correct", 1)
            display.text(self.screen, self.font, "correct",
                         "center", "center", (0, 255, 0))
        else:
            df.set_value(i, "correct", 0)
            display.text(self.screen, self.font, "incorrect",
                         "center", "center", (255, 0, 0))

        pygame.display.flip()

        display.wait(self.feedback_duration)

        # Display blank screen (ITI)
        display.blank_screen(self.screen, self.background, self.ITI)

    def display_sequence(self, sequence):
        for i, number in enumerate(sequence):
            # Display number
            self.screen.blit(self.background, (0, 0))
            display.text(self.screen, self.stim_font, number,
                         "center", "center")
            pygame.display.flip()

            display.wait(self.stim_duration)

            # Display blank screen
            display.blank_screen(self.screen, self.background,
                                 self.between_stim_duration)

    def run(self):
        # Instructions screen
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font,
                     "You will see a sequence of numbers, one at a time. "
                     "Try your best to memorize them",
                     100, 100)

        display.text(self.screen, self.stim_font, "8 - 5 - 4 - 1 - 0 - 9",
                     "center", 200)

        display.text(self.screen, self.font,
                     "You will then be shown a single test number in blue",
                     100, 300)

        display.text(self.screen, self.stim_font, "0",
                     "center", 400, (0, 0, 255))

        display.text(self.screen, self.font,
                     "If this number was in the original sequence, "
                     "press the LEFT arrow",
                     100, 550)

        display.text(self.screen, self.font,
                     "If this number was NOT in the original sequence, "
                     "press the RIGHT arrow",
                     100, 650)

        display.text(self.screen, self.font,
                     "Try to do this as quickly, "
                     "and as accurately, as possible",
                     100, 750)

        display.text_space(self.screen, self.font, "center", 900)

        pygame.display.flip()

        display.wait_for_space()

        # Practice ready screen
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font,
                     "We will begin with some practice trials...",
                     "center", "center")

        display.text_space(self.screen, self.font,
                           "center", self.screen_y/2 + 100)

        pygame.display.flip()

        display.wait_for_space()

        # Practice trials
        for i, r in self.practice_trials.iterrows():
            self.display_trial(self.practice_trials, i, r, "practice")

        # Main trials ready screen
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font, "End of practice trials.",
                     100, 100)
        display.text(self.screen, self.font, "You may move on to the main "
                                             "trials when you're ready",
                     100, 300)

        display.text(self.screen, self.font, "Remember to respond as quickly "
                                             "and as accurately as possible",
                     100, 500)
        display.text(self.screen, self.font, "Your reaction time and accuracy"
                                             " will be recorded",
                     100, 600)
        display.text_space(self.screen, self.font,
                           "center", 800)

        pygame.display.flip()

        display.wait_for_space()

        # Main trials
        for i, block in enumerate(self.blocks):
            for j, r in block.iterrows():
                self.display_trial(block, j, r, "main")

            # If this is not the final block, show instructions for next block
            if i != len(self.blocks)-1:
                display.text(self.screen, self.font, "End of block.", 100, 200)
                display.text(self.screen, self.font,
                             "Take a short break, and press space when you're "
                             "ready to start the next block...", 100, 400)
                display.text_space(self.screen, self.font,
                                   "center", 700)

                pygame.display.flip()

                display.wait_for_space()

        # End screen
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font, "End of task", "center", "center")
        display.text_space(self.screen, self.font,
                           "center", (self.screen_y / 2) + 100)
        pygame.display.flip()

        display.wait_for_space()

        # Concatenate blocks and add trial numbers
        all_data = pd.concat(self.blocks)
        all_data['trialNum'] = range(1, len(all_data)+1)

        print "- Sternberg Task complete"

        return all_data
