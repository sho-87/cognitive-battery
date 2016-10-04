import sys
import os
import time
import pandas as pd
import numpy as np
import pygame

from pygame.locals import *
from itertools import product

from utils import display


class ANT(object):
    def __init__(self, screen, background, blocks=3):
        # Get the pygame display window
        self.screen = screen
        self.background = background

        # Sets font and font size
        self.font = pygame.font.SysFont("arial", 30)

        # Get screen info
        self.screen_x = self.screen.get_width()
        self.screen_y = self.screen.get_height()

        # Fill background
        self.background.fill((255, 255, 255))
        pygame.display.set_caption("ANT Task")
        pygame.mouse.set_visible(0)

        # Experiment options
        self.NUM_BLOCKS = blocks
        self.FIXATION_DURATION_RANGE = (400, 1600)  # Range of fixation times
        self.CUE_DURATION = 100
        self.PRE_STIM_FIXATION_DURATION = 400
        self.TARGET_OFFSET = 31  # Stimulus vertical offset
        self.FLANKER_DURATION = 1700
        self.FEEDBACK_DURATION = 1000
        self.ITI_MAX = 3500

        # Specify factor levels, and task timings as used by Fan et al. (2002).
        self.CONGRUENCY_LEVELS = ("congruent", "incongruent", 'neutral')
        self.CUE_LEVELS = ("nocue", "center", "spatial", 'double')
        self.LOCATION_LEVELS = ('top', 'bottom')
        self.DIRECTION_LEVELS = ('left', 'right')

        # Create level combinations
        # Level combinations give us 48 trials.
        self.combinations = list(
            product(self.CONGRUENCY_LEVELS, self.CUE_LEVELS,
                    self.LOCATION_LEVELS, self.DIRECTION_LEVELS))

        # Get images
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.image_path = os.path.join(self.base_dir, "images", "ANT")

        self.img_left_congruent = pygame.image.load(
            os.path.join(self.image_path, 'left_congruent.png'))
        self.img_left_incongruent = pygame.image.load(
            os.path.join(self.image_path, 'left_incongruent.png'))
        self.img_right_congruent = pygame.image.load(
            os.path.join(self.image_path, 'right_congruent.png'))
        self.img_right_incongruent = pygame.image.load(
            os.path.join(self.image_path, 'right_incongruent.png'))
        self.img_left_neutral = pygame.image.load(
            os.path.join(self.image_path, 'left_neutral.png'))
        self.img_right_neutral = pygame.image.load(
            os.path.join(self.image_path, 'right_neutral.png'))

        self.img_fixation = pygame.image.load(
            os.path.join(self.image_path, 'fixation.png'))
        self.img_cue = pygame.image.load(
            os.path.join(self.image_path, 'cue.png'))

        # Get image dimensions
        self.flanker_w, self.flanker_h =\
            self.img_left_incongruent.get_rect().size

        self.fixation_w, self.fixation_h = self.img_fixation.get_rect().size

        # Create output dataframe
        self.all_data = pd.DataFrame()

    def create_block(self, block_num, combinations, trial_type):
        if trial_type == "main":
            cur_combinations = combinations * 2
            np.random.shuffle(cur_combinations)
        else:
            np.random.shuffle(combinations)
            cur_combinations = combinations[:len(combinations) / 2]

        # Add combinations to dataframe
        cur_block = pd.DataFrame(data=cur_combinations, columns=(
            'congruency', 'cue', 'location', 'direction'))

        # Add timing info to dataframe
        cur_block["block"] = block_num + 1
        cur_block["fixationTime"] = [x for x in np.random.randint(
            self.FIXATION_DURATION_RANGE[0], self.FIXATION_DURATION_RANGE[1],
            len(cur_combinations))]

        return cur_block

    def display_flanker(self, flanker_type, location, direction):
        # Left flanker
        if direction == "left":
            if flanker_type == "congruent":
                stimulus = self.img_left_congruent
            elif flanker_type == "incongruent":
                stimulus = self.img_left_incongruent
            else:
                stimulus = self.img_left_neutral
        # Right flanker
        else:
            if flanker_type == "congruent":
                stimulus = self.img_right_congruent
            elif flanker_type == "incongruent":
                stimulus = self.img_right_incongruent
            else:
                stimulus = self.img_right_neutral

        # Offset the flanker stimulus to above/below fixation
        if location == "top":
            display.image(
                self.screen, stimulus, "center",
                self.screen_y/2 - self.flanker_h - self.TARGET_OFFSET)
        elif location == "bottom":
            display.image(self.screen, stimulus, "center",
                          self.screen_y / 2 + self.TARGET_OFFSET)

    def display_trial(self, trial_num, data, trial_type):
        # Check for a quit press after stimulus was shown
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_F9:
                return self.all_data
            elif event.type == KEYDOWN and event.key == K_F12:
                sys.exit(0)

        # Display fixation
        self.screen.blit(self.background, (0, 0))
        display.image(self.screen, self.img_fixation, "center", "center")
        pygame.display.flip()

        display.wait(data["fixationTime"][trial_num])

        # Display cue
        self.screen.blit(self.background, (0, 0))

        cue_type = data["cue"][trial_num]

        if cue_type == "nocue":
            # Display fixation in the center
            display.image(self.screen, self.img_fixation, "center", "center")
        elif cue_type == "center":
            # Display cue in the center
            display.image(self.screen, self.img_cue, "center", "center")
        elif cue_type == "double":
            # Display fixation in the center
            display.image(self.screen, self.img_fixation, "center", "center")

            # Display cue above and below fixation
            display.image(
                self.screen, self.img_cue, "center",
                self.screen_y/2 - self.fixation_h - self.TARGET_OFFSET)
            display.image(self.screen, self.img_cue,
                          "center", self.screen_y / 2 + self.TARGET_OFFSET)
        elif cue_type == "spatial":
            cue_location = data["location"][trial_num]

            # Display fixation in the center
            display.image(self.screen, self.img_fixation, "center", "center")

            # Display cue at target location
            if cue_location == "top":
                display.image(
                    self.screen, self.img_cue, "center",
                    self.screen_y/2 - self.fixation_h - self.TARGET_OFFSET)
            elif cue_location == "bottom":
                display.image(self.screen, self.img_cue, "center",
                              self.screen_y / 2 + self.TARGET_OFFSET)

        pygame.display.flip()

        # Display cue for certain duration
        display.wait(self.CUE_DURATION)

        # Prestim interval with fixation
        self.screen.blit(self.background, (0, 0))
        display.image(self.screen, self.img_fixation, "center", "center")
        pygame.display.flip()

        display.wait(self.PRE_STIM_FIXATION_DURATION)

        # Display flanker target
        self.screen.blit(self.background, (0, 0))
        display.image(self.screen, self.img_fixation, "center", "center")

        self.display_flanker(data["congruency"][trial_num],
                             data["location"][trial_num],
                             data["direction"][trial_num])

        pygame.display.flip()

        start_time = int(round(time.time() * 1000))

        # Clear the event queue before checking for responses
        pygame.event.clear()
        response = "NA"
        wait_response = True
        while wait_response:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_LEFT:
                    response = "left"
                    wait_response = False
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    response = "right"
                    wait_response = False
                elif event.type == KEYDOWN and event.key == K_F9:
                    return self.all_data
                elif event.type == KEYDOWN and event.key == K_F12:
                    sys.exit(0)

            end_time = int(round(time.time() * 1000))

            # If time limit has been reached, consider it a missed trial
            if end_time - start_time >= self.FLANKER_DURATION:
                wait_response = False

        # Store reaction time and response
        rt = int(round(time.time() * 1000)) - start_time
        data.set_value(trial_num, 'RT', rt)
        data.set_value(trial_num, 'response', response)

        correct = 1 if response == data["direction"][trial_num] else 0
        data.set_value(trial_num, 'correct', correct)

        # Display feedback if practice trials
        if trial_type == "practice":
            self.screen.blit(self.background, (0, 0))
            if correct == 1:
                display.text(self.screen, self.font, "correct",
                             "center", "center", (0, 255, 0))
            else:
                display.text(self.screen, self.font, "incorrect",
                             "center", "center", (255, 0, 0))

            pygame.display.flip()

            display.wait(self.FEEDBACK_DURATION)

        # Display fixation during ITI
        self.screen.blit(self.background, (0, 0))
        display.image(self.screen, self.img_fixation, "center", "center")

        pygame.display.flip()

        iti = self.ITI_MAX - rt - data["fixationTime"][trial_num]
        data.set_value(trial_num, 'ITI', iti)

        display.wait(iti)

    def run_block(self, blockNum, totalBlocks, type):
        self.curBlock = self.create_block(blockNum, self.combinations, type)

        for j in range(self.curBlock.shape[0]):
            self.display_trial(j, self.curBlock, type)

        if type == "main":
            # add block data to all_data
            self.all_data = pd.concat([self.all_data, self.curBlock])

        # end of block screen
        if blockNum != totalBlocks - 1:
            self.blockEnd = True
            while self.blockEnd:
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        self.blockEnd = False

                self.screen.blit(self.background, (0, 0))

                self.blockText = self.font.render(
                    "End of current block. Start next block when you're ready...",
                    1, (0, 0, 0))
                self.screen.blit(self.blockText, (100, self.screen_y / 2))

                display.text_space(self.screen, self.font,
                                   100, (self.screen_y / 2) + 100)

                pygame.display.flip()

    def run(self):
        # Instructions
        self.screen.blit(self.background, (0, 0))

        self.title = self.font.render("Attentional Network Test",
                                      1, (0, 0, 0))
        self.titleW = self.title.get_rect().width
        self.screen.blit(self.title, (
            self.screen_x / 2 - self.titleW / 2, self.screen_y / 2 - 300))

        self.line1 = self.font.render(
            "Keep your eyes on the fixation cross at the start of each trial:",
            1, (0, 0, 0))
        self.screen.blit(self.line1, (100, self.screen_y / 2 - 200))

        self.screen.blit(self.img_fixation, (
            self.screen_x / 2 - self.fixation_w / 2, self.screen_y / 2 - 150))

        self.line2 = self.font.render(
            "Then, a set of arrows will appear somewhere on the screen:", 1,
            (0, 0, 0))
        self.screen.blit(self.line2, (100, self.screen_y / 2 - 100))

        self.screen.blit(self.img_left_incongruent, (
            self.screen_x / 2 - self.flanker_w / 2, self.screen_y / 2 - 50))

        self.line3 = self.font.render(
            "Use the left/right arrow keys to indicate the direction of the CENTER arrow only.",
            1, (0, 0, 0))
        self.screen.blit(self.line3, (100, self.screen_y / 2))

        self.line4 = self.font.render(
            "In example above, the correct answer is LEFT.", 1, (0, 0, 0))
        self.screen.blit(self.line4, (100, self.screen_y / 2 + 50))

        display.text_space(self.screen, self.font,
                           100, (self.screen_y / 2) + 300)

        self.instructions = True
        while self.instructions:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.instructions = False
                elif event.type == KEYDOWN and event.key == K_F12:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()

        # Instructions Practice
        self.instructionsPractice = True
        while self.instructionsPractice:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.instructionsPractice = False
                elif event.type == KEYDOWN and event.key == K_F12:
                    pygame.quit()
                    sys.exit()

                self.screen.blit(self.background, (0, 0))
                self.practiceInstructions = self.font.render(
                    "We will begin with a few practice trials...", 1,
                    (0, 0, 0))
                self.screen.blit(self.practiceInstructions,
                                 (100, self.screen_y / 2))

                display.text_space(self.screen, self.font,
                                   100, (self.screen_y / 2) + 100)

                pygame.display.flip()

        # Practice trials
        for i in range(1):
            self.run_block(i, 1, "practice")

        # Instructions Practice End
        self.practiceEndScreen = True
        while self.practiceEndScreen:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.practiceEndScreen = False

            self.screen.blit(self.background, (0, 0))
            self.practiceEndLine = self.font.render(
                "We will now begin the main trials...", 1, (0, 0, 0))
            self.screen.blit(self.practiceEndLine,
                             (100, self.screen_y / 2 - 50))

            self.practiceEndLine2 = self.font.render(
                "You will not receive feedback after each trial.", 1,
                (0, 0, 0))
            self.screen.blit(self.practiceEndLine2,
                             (100, self.screen_y / 2 + 50))

            display.text_space(self.screen, self.font,
                               100, (self.screen_y / 2) + 200)

            pygame.display.flip()

        # Main task
        for i in range(self.NUM_BLOCKS):
            self.run_block(i, self.NUM_BLOCKS, "main")

        # create trial number column
        self.trialNums = np.arange(1, self.all_data.shape[0] + 1)
        self.all_data["trial"] = self.trialNums

        # rearrange the dataframe
        self.columns = ['trial', 'block', 'congruency', 'cue', 'location',
                        'fixationTime', 'ITI', 'direction', 'response',
                        'correct', 'RT']
        self.all_data = self.all_data[self.columns]

        # End screen
        self.endScreen = True
        while self.endScreen:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.endScreen = False

            self.screen.blit(self.background, (0, 0))
            self.endLine = self.font.render("End of task.", 1,
                                            (0, 0, 0))
            self.screen.blit(self.endLine, (100, self.screen_y / 2))

            display.text_space(self.screen, self.font,
                               100, (self.screen_y / 2) + 100)

            pygame.display.flip()

        print "- ANT complete"

        return self.all_data
