import os
import sys
import time
import random
import pandas as pd
import pygame

from pygame.locals import *
from utils import display


class SART(object):
    def __init__(self, screen, background):
        # Get the pygame display window
        self.screen = screen
        self.background = background

        # Set font and font size
        self.font = pygame.font.SysFont("arial", 30)
        self.stim_fonts = []

        # Get screen info
        self.screen_x = self.screen.get_width()
        self.screen_y = self.screen.get_height()

        # Fill background
        self.background.fill((0, 0, 0))
        pygame.display.set_caption("SART")
        pygame.mouse.set_visible(0)

        # Experiment options
        self.BLANK_DURATION = 500
        self.STIM_DURATION = 250
        self.MASK_DURATION = 900
        self.STIMSIZES_PT = (48, 72, 94, 100, 120)  # in point
        self.STIMSIZES_MM = (12, 18, 23, 24, 29)  # in mm from original paper

        # Generate font renderers of different sizes
        for size in self.STIMSIZES_PT:
            self.stim_fonts.append(pygame.font.SysFont("arial", size))

        # Get mask image
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.image_path = os.path.join(self.base_dir, "images", "SART")

        # Use the 29mm mask image (as described by Robertson 1997)
        self.img_mask = pygame.image.load(
            os.path.join(self.image_path, 'mask_29.png'))

        # Create trial sequence
        self.number_set = range(1, 10)*25  # Numbers 1-9
        random.shuffle(self.number_set)
        self.trial_num = range(1, len(self.number_set)+1)

        # Create output dataframe
        self.all_data = pd.DataFrame()
        self.all_data["trial"] = self.trial_num
        self.all_data["stimulus"] = self.number_set

    def display_trial(self, i, data):
        # Randomly choose font size for this trial
        size_index = random.randint(0, len(self.stim_fonts)-1)
        trial_font = self.stim_fonts[size_index]

        key_press = 0
        data.set_value(i, 'RT', 1150)

        # Display number
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, trial_font, str(data["stimulus"][i]),
                     "center", "center", (255, 255, 255))
        pygame.display.flip()

        # Get start time in ms
        start_time = int(round(time.time() * 1000))

        # Clear the event queue before checking for responses
        pygame.event.clear()
        wait_response = True
        while wait_response:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    key_press = 1
                    data.set_value(i, 'RT',
                                   int(round(time.time() * 1000)) - start_time)
                elif event.type == KEYDOWN and event.key == K_F12:
                    sys.exit(0)

            end_time = int(round(time.time() * 1000))

            # Stop this loop if stim duration has passed
            if end_time - start_time >= self.STIM_DURATION:
                wait_response = False

        # Display mask
        self.screen.blit(self.background, (0, 0))
        display.image(self.screen, self.img_mask, "center", "center")
        pygame.display.flip()

        wait_response = True
        while wait_response:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    if key_press == 0:
                        key_press = 1
                        data.set_value(
                            i, 'RT',
                            int(round(time.time() * 1000)) - start_time)
                elif event.type == KEYDOWN and event.key == K_F12:
                    sys.exit(0)

            end_time = int(round(time.time() * 1000))

            # Stop this loop if mask duration has passed
            if end_time - start_time >= self.MASK_DURATION:
                wait_response = False

        # Check if response is correct
        if data["stimulus"][i] == 3:
            if key_press == 0:
                accuracy = 1
            else:
                accuracy = 0
        else:
            if key_press == 0:
                accuracy = 0
            else:
                accuracy = 1

        # Store key press data in dataframe
        data.set_value(i, 'key press', key_press)
        data.set_value(i, 'accuracy', accuracy)
        data.set_value(i, 'stimSize', self.STIMSIZES_PT[size_index])

    def run(self):
        # Instructions
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font, "SART",
                     "center", self.screen_y/2 - 250, (255, 255, 255))

        display.text(self.screen, self.font,
                     "Numbers will appear in the center of the screen.",
                     100, self.screen_y/2 - 150, (255, 255, 255))

        display.text(self.screen, self.font,
                     "Press the spacebar after you see a number.",
                     100, self.screen_y/2 - 50, (255, 255, 255))

        display.text(self.screen, self.font,
                     "However, if the number is a 3, "
                     "do NOT press the spacebar.",
                     100, self.screen_y/2 + 50, (255, 255, 255))

        display.text(self.screen, self.font,
                     "Please respond as quickly, "
                     "and as accurately, as possible",
                     100, self.screen_y/2 + 150, (255, 255, 255))

        display.text_space(self.screen, self.font,
                           "center", self.screen_y/2 + 300, (255, 255, 255))

        pygame.display.flip()

        display.wait_for_space()

        # Instructions Practice
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font,
                     "We will begin with a few practice trials...",
                     "center", "center", (255, 255, 255))

        display.text_space(self.screen, self.font,
                           "center",
                           self.screen_y/2 + 100, (255, 255, 255))

        pygame.display.flip()

        display.wait_for_space()

        # Blank screen
        display.blank_screen(self.screen, self.background, self.BLANK_DURATION)

        # Show practice trials
        practice_trials = pd.DataFrame([5, 7, 7, 3, 9, 2, 1, 3, 8, 6],
                                       columns=['stimulus'])

        for i in range(practice_trials.shape[0]):
            self.display_trial(i, practice_trials)

        # Practice end screen
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font,
                     "End of practice trials",
                     "center", self.screen_y/2 - 100, (255, 255, 255))

        display.text(self.screen, self.font,
                     "We will now begin the main trials...",
                     "center", "center", (255, 255, 255))

        display.text_space(self.screen, self.font,
                           "center", self.screen_y/2 + 100, (255, 255, 255))

        pygame.display.flip()

        display.wait_for_space()

        # Blank screen
        display.blank_screen(self.screen, self.background, self.BLANK_DURATION)

        # Show main trials
        for i in range(self.all_data.shape[0]):
            self.display_trial(i, self.all_data)

        # Rearrange dataframe
        columns = ['trial', 'stimulus', 'stimSize', 'RT', 'key press',
                   'accuracy']
        self.all_data = self.all_data[columns]

        # End screen
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font,
                     "End of task", "center", "center", (255, 255, 255))

        display.text_space(self.screen, self.font,
                           "center", self.screen_y/2 + 100, (255, 255, 255))

        pygame.display.flip()

        display.wait_for_space()

        print "- SART complete"

        return self.all_data
