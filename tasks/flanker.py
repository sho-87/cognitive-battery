import sys
import time
import pandas as pd
import numpy as np
import pygame

from pygame.locals import *
from itertools import product
from utils import display


class Flanker(object):
    def __init__(self, screen, background, dark_mode=False,
                 blocks_compat=1, blocks_incompat=0, block_order="compatible"):
        # Get the pygame display window
        self.screen = screen
        self.background = background

        # Sets font and font size
        self.font = pygame.font.SysFont("arial", 30)
        self.font_stim = pygame.font.SysFont("arial", 100)

        # Set colours
        if dark_mode:
            self.colour_bg = (0, 0, 0)
            self.colour_font = (255, 255, 255)
        else:
            self.colour_bg = (255, 255, 255)
            self.colour_font = (0, 0, 0)

        # Get screen info
        self.screen_x = self.screen.get_width()
        self.screen_y = self.screen.get_height()

        # Fill background
        self.background.fill(self.colour_bg)
        pygame.display.set_caption("Eriksen Flanker Task")
        pygame.mouse.set_visible(0)

        # Experiment options
        self.BLOCK_ORDER = block_order
        self.BLOCKS_COMPAT = blocks_compat
        self.BLOCKS_INCOMPAT = blocks_incompat
        self.FIXATION_DURATION = 1000
        self.FLANKER_DURATION = 200
        self.MAX_RESPONSE_TIME = 1500
        self.FEEDBACK_DURATION = 1500
        self.ITI = 1500

        # Set stimuli
        self.flanker_stim = {"left": {"congruent": "< < < < <",
                                      "incongruent": "> > < > >"},
                             "right": {"congruent": "> > > > >",
                                       "incongruent": "< < > < <"}}

        # Specify factor levels
        self.CONGRUENCY_LEVELS = ("congruent", "incongruent")
        self.DIRECTION_LEVELS = ("left", "right")

        # Create level combinations
        # Level combinations give us 4 trials.
        self.combinations = list(product(self.CONGRUENCY_LEVELS, self.DIRECTION_LEVELS))

        # Create output dataframe
        self.all_data = pd.DataFrame()

    def create_block(self, block_num, combinations, trial_type, compatibility):
        if trial_type == "main":
            cur_combinations = combinations * 1  # 30 - 120 total trials
        else:
            cur_combinations = combinations * 1  # 5 - 20 practice trials

        # Add shuffled combinations to dataframe
        np.random.shuffle(cur_combinations)
        cur_block = pd.DataFrame(data=cur_combinations,
                                 columns=("congruency", "direction"))

        # Add timing info to dataframe
        cur_block["block"] = block_num + 1
        cur_block["compatibility"] = compatibility

        return cur_block

    def display_flanker(self, flanker_type, direction):
        stimulus = self.flanker_stim[direction][flanker_type]
        display.text(self.screen, self.font_stim, stimulus, "center", "center", self.colour_font)

    def display_trial(self, trial_num, data):
        # Check for a quit press after stimulus was shown
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_F12:
                sys.exit(0)

        # Display fixation
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font, "+", "center", "center", self.colour_font)
        pygame.display.flip()

        display.wait(self.FIXATION_DURATION)

        # Display flanker stimulus
        self.screen.blit(self.background, (0, 0))
        self.display_flanker(data["congruency"][trial_num],
                             data["direction"][trial_num])
        pygame.display.flip()

        # Clear the event queue before checking for responses
        start_time = int(round(time.time() * 1000))
        pygame.event.clear()
        response = "NA"
        too_slow = False
        wait_response = True
        while wait_response:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_LEFT:
                    response = "left"
                    wait_response = False
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    response = "right"
                    wait_response = False
                elif event.type == KEYDOWN and event.key == K_F12:
                    sys.exit(0)

            end_time = int(round(time.time() * 1000))

            if end_time - start_time >= self.FLANKER_DURATION:
                self.screen.blit(self.background, (0, 0))
                pygame.display.flip()

            if end_time - start_time >= self.MAX_RESPONSE_TIME:
                # If time limit has been reached, consider it a missed trial
                wait_response = False
                too_slow = True

        # Store reaction time and response
        rt = int(round(time.time() * 1000)) - start_time
        data.set_value(trial_num, "RT", rt)
        data.set_value(trial_num, "response", response)

        if data["compatibility"][trial_num] == "compatible":
            correct = 1 if response == data["direction"][trial_num] else 0
        else:
            correct = 1 if response != data["direction"][trial_num] else 0
        data.set_value(trial_num, "correct", correct)

        # Display feedback
        self.screen.blit(self.background, (0, 0))
        if too_slow:
            display.text(self.screen, self.font, "too slow",
                         "center", "center", self.colour_font)
        else:
            if correct == 1:
                display.text(self.screen, self.font, "correct",
                             "center", "center", (0, 255, 0))
            else:
                display.text(self.screen, self.font, "incorrect",
                             "center", "center", (255, 0, 0))
        pygame.display.flip()

        display.wait(self.FEEDBACK_DURATION)

        if trial_num != data.shape[0] - 1:
            # Display fixation
            self.screen.blit(self.background, (0, 0))
            display.text(self.screen, self.font, "+", "center", "center", self.colour_font)
            pygame.display.flip()
            display.wait(self.ITI)

    def run_block(self, block_num, total_blocks, block_type, compatibility, second_half=False):
        cur_block = self.create_block(block_num, self.combinations, block_type, compatibility)

        for i in range(cur_block.shape[0]):
            self.display_trial(i, cur_block)

        if block_type == "main":
            # Add block data to all_data
            self.all_data = pd.concat([self.all_data, cur_block])

        if second_half:
            total_blocks = self.BLOCKS_INCOMPAT + self.BLOCKS_COMPAT

        # End of block screen
        if block_num != total_blocks - 1:  # If not the final block
            self.screen.blit(self.background, (0, 0))
            display.text(self.screen, self.font,
                         "End of current block. "
                         "Start next block when you're ready...",
                         100, "center", self.colour_font)
            display.text_space(self.screen, self.font,
                               "center", (self.screen_y/2) + 100, self.colour_font)
            pygame.display.flip()

            display.wait_for_space()

    def run(self):
        if self.BLOCK_ORDER == "choose":
            # If the order is "choose" but one of the block types has a 0, then dont show choose screen
            if self.BLOCKS_COMPAT == 0:
                self.BLOCK_ORDER = "incompatible"
            elif self.BLOCKS_INCOMPAT == 0:
                self.BLOCK_ORDER = "compatible"
            else:
                self.screen.blit(self.background, (0, 0))
                display.text(self.screen, self.font, "Choose block order:",
                             100, self.screen_y/2 - 300, self.colour_font)
                display.text(self.screen, self.font,
                             "1 - Compatible first",
                             100, self.screen_y/2 - 200, self.colour_font)
                display.text(self.screen, self.font,
                             "2 - Incompatible first",
                             100, self.screen_y/2 - 150, self.colour_font)
                pygame.display.flip()

                wait_response = True
                while wait_response:
                    for event in pygame.event.get():
                        if event.type == KEYDOWN and event.key == K_1:
                            self.BLOCK_ORDER = "compatible"
                            wait_response = False
                        elif event.type == KEYDOWN and event.key == K_2:
                            self.BLOCK_ORDER = "incompatible"
                            wait_response = False
                        elif event.type == KEYDOWN and event.key == K_F12:
                            sys.exit(0)

        # Set block order
        if self.BLOCK_ORDER == "compatible":
            self.block_type_list = (["compatible"] * self.BLOCKS_COMPAT) + (["incompatible"] * self.BLOCKS_INCOMPAT)
        elif self.BLOCK_ORDER == "incompatible":
            self.block_type_list = (["incompatible"] * self.BLOCKS_INCOMPAT) + (["compatible"] * self.BLOCKS_COMPAT)

        # Instructions
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font, "Eriksen Flanker Task",
                     "center", self.screen_y/2 - 300, self.colour_font)
        display.text(self.screen, self.font,
                     "Keep your eyes on the fixation cross at the "
                     "start of each trial:",
                     100, self.screen_y/2 - 200, self.colour_font)
        display.text(self.screen, self.font, "+", "center", self.screen_y/2 - 150, self.colour_font)
        display.text(self.screen, self.font,
                     "A set of arrows will appear:",
                     100, self.screen_y/2 - 100, self.colour_font)
        display.text(self.screen, self.font_stim, self.flanker_stim["left"]["incongruent"],
                     "center", self.screen_y/2 - 50, self.colour_font)

        if self.block_type_list[0] == "compatible":
            display.text(self.screen, self.font,
                         "Use the Left / Right arrow keys to indicate "
                         "the direction of the CENTER arrow.",
                         100, self.screen_y/2 + 70, self.colour_font)
            display.text(self.screen, self.font,
                         "In example above, you should press the Left arrow.",
                         100, self.screen_y/2 + 120, self.colour_font)
        elif self.block_type_list[0] == "incompatible":
            display.text(self.screen, self.font,
                         "Use the Left / Right arrow keys to indicate "
                         "the OPPOSITE direction of the CENTER arrow.",
                         100, self.screen_y/2 + 70, self.colour_font)
            display.text(self.screen, self.font,
                         "In example above, you should press the Right arrow.",
                         100, self.screen_y/2 + 120, self.colour_font)

        display.text_space(self.screen, self.font,
                           "center", (self.screen_y/2) + 300, self.colour_font)
        pygame.display.flip()

        display.wait_for_space()

        # Instructions Practice
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font,
                     "We'll begin with a some practice trials...",
                     "center", "center", self.colour_font)
        display.text_space(self.screen, self.font,
                           "center", self.screen_y/2 + 100, self.colour_font)
        pygame.display.flip()

        display.wait_for_space()

        # Practice trials
        self.run_block(0, 1, "practice", self.block_type_list[0])

        # Instructions Practice End
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font,
                     "We will now begin the main trials...",
                     100, self.screen_y/2, self.colour_font)
        display.text_space(self.screen, self.font,
                           "center", self.screen_y/2 + 200, self.colour_font)
        pygame.display.flip()

        display.wait_for_space()

        # Main task second half
        if self.block_type_list[0] == "compatible":
            for i in range(self.BLOCKS_COMPAT):
                self.run_block(i, self.BLOCKS_COMPAT, "main", self.block_type_list[0])
        elif self.block_type_list[0] == "incompatible":
            for i in range(self.BLOCKS_INCOMPAT):
                self.run_block(i, self.BLOCKS_INCOMPAT, "main", self.block_type_list[0])

        # Second half (if more than one compatibility type)
        if self.block_type_list[0] != self.block_type_list[-1]:
            # Practice instructions
            self.screen.blit(self.background, (0, 0))
            display.text(self.screen, self.font,
                         "Second half instructions",
                         100, self.screen_y/2, self.colour_font)
            display.text_space(self.screen, self.font,
                               "center", self.screen_y/2 + 200, self.colour_font)
            pygame.display.flip()

            display.wait_for_space()

            # Practice trials
            self.run_block(0, 1, "practice", self.block_type_list[-1])

            # Instructions Practice End
            self.screen.blit(self.background, (0, 0))
            display.text(self.screen, self.font,
                         "We will now begin the main trials...",
                         100, self.screen_y/2, self.colour_font)
            display.text_space(self.screen, self.font,
                               "center", self.screen_y/2 + 200, self.colour_font)
            pygame.display.flip()
            display.wait_for_space()

            # Main task
            if self.block_type_list[-1] == "compatible":
                for i in range(self.BLOCKS_COMPAT):
                    self.run_block(self.BLOCKS_INCOMPAT + i, self.BLOCKS_COMPAT, "main", self.block_type_list[-1], True)
            elif self.block_type_list[-1] == "incompatible":
                for i in range(self.BLOCKS_INCOMPAT):
                    self.run_block(self.BLOCKS_COMPAT + i, self.BLOCKS_INCOMPAT, "main", self.block_type_list[-1], True)

        # Create trial number column
        self.all_data["trial"] = list(range(1, len(self.all_data) + 1))

        # Rearrange the dataframe
        columns = ["trial", "block", "compatibility", "congruency", "direction",
                   "response", "correct", "RT"]
        self.all_data = self.all_data[columns]

        # End screen
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font, "End of task", "center", "center", self.colour_font)
        display.text_space(self.screen, self.font,
                           "center", self.screen_y/2 + 100, self.colour_font)
        pygame.display.flip()

        display.wait_for_space()

        print("- Flanker complete")

        return self.all_data
