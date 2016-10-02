import os
import time
import random
import pandas as pd
import pygame

from pygame.locals import *
from itertools import product
from sys import exit


class Sternberg(object):
    def __init__(self, screen, blocks=2):
        # Get the pygame display window
        self.screen = screen

        # Sets font and font size
        self.instructions_font = pygame.font.SysFont("arial", 30)

        # Get screen info
        self.screen_x = self.screen.get_width()
        self.screen_y = self.screen.get_height()

        # Fills background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))
        pygame.display.set_caption("Sternberg Task")
        pygame.mouse.set_visible(0)

        # Experiment options
        # Timings are taken from Sternberg (1966)
        # Block sizes are taken from Martins (2012)
        self.num_blocks = blocks
        self.stim_duration = 1200
        self.between_stim_duration = 250
        self.probe_warn = 2000
        self.feedback_duration = 1000
        self.ITI = 750
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

    def run(self):

        # Concatenate blocks and add trial numbers
        all_data = pd.concat(self.blocks)
        all_data['trialNum'] = range(1, len(all_data)+1)

        print "- Sternberg Task complete"

        return all_data
