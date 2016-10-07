import sys
import time
import random
import pandas as pd
import numpy as np
import pygame

from pygame.locals import *
from utils import display


class DigitspanBackwards(object):
    def __init__(self, screen, background):
        # Get the pygame display window
        self.screen = screen
        self.background = background

        # Set fonts and font sizes
        self.font = pygame.font.SysFont("arial", 30)
        self.stimulus_font = pygame.font.SysFont("arial", 80)

        # get screen info
        self.screen_x = self.screen.get_width()
        self.screen_y = self.screen.get_height()

        # Fill background
        self.background.fill((255, 255, 255))
        pygame.display.set_caption("Backwards Digitspan")
        pygame.mouse.set_visible(0)

        # Experiment options
        self.STIM_DURATION = 1000  # Duration of each digit
        self.INTER_NUMBER_DURATION = 100  # Time between numbers
        self.NUMBERS_USED = range(1, 10)  # Set of digits that can be used
        self.START_LENGTH = 3  # Length of smallest sequence
        self.END_LENGTH = 9  # Length of largest sequence
        self.NUM_REPEATS = 2  # Num of times each sequence length is repeated

        self.num_lengths = self.END_LENGTH - self.START_LENGTH + 1

        # Generate all possible number sequence lengths for experiment
        self.digit_lengths = np.asarray(
            [j for i in range(self.START_LENGTH, self.END_LENGTH + 1) for j in
             [i] * self.NUM_REPEATS])

        # Create main dataframe
        self.all_data = pd.DataFrame()
        self.all_data["trial"] = range(1,
                                       self.num_lengths * self.NUM_REPEATS + 1)
        self.all_data["length"] = self.digit_lengths

        # Create digit sequences
        for i in range(len(self.all_data)):
            generated_sequence = random.sample(self.NUMBERS_USED,
                                               self.all_data['length'][i])
            self.all_data.set_value(
                i, 'sequence', ''.join(str(n) for n in generated_sequence))

    def display_numbers(self, i, data):
        for number in data['sequence'][i]:
            self.screen.blit(self.background, (0, 0))
            display.text(self.screen, self.stimulus_font, number,
                         "center", "center")
            pygame.display.flip()

            display.wait(self.STIM_DURATION)

            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

            display.wait(self.INTER_NUMBER_DURATION)

        return data['sequence'][i]

    def number_entry(self):
        user_sequence = ""

        # Clear the event queue before checking for responses
        pygame.event.clear()

        entry = True
        while entry:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    entry = False
                elif event.type == KEYDOWN and event.key == K_F12:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                    if user_sequence:
                        # Remove last number in entered string
                        user_sequence = user_sequence[:-1]
                elif event.type == KEYDOWN:
                    try:
                        # Only allow key press of used numbers
                        key_pressed = int(pygame.key.name(event.key))
                        if key_pressed in self.NUMBERS_USED:
                            user_sequence += pygame.key.name(event.key)
                    except ValueError:
                        pass

            self.screen.blit(self.background, (0, 0))
            display.text(self.screen, self.font,
                         "Type the sequence in backwards order:",
                         50, self.screen_y/4)

            display.text(self.screen, self.stimulus_font, user_sequence,
                         "center", "center")

            pygame.display.flip()

        return user_sequence

    def run(self):
        # Instructions
        self.screen.blit(self.background, (0, 0))

        self.title = self.font.render("Backwards Digit Span", 1,
                                      (0, 0, 0))
        self.titleW = self.title.get_rect().width
        self.screen.blit(self.title, (
            self.screen_x / 2 - self.titleW / 2, self.screen_y / 2 - 300))

        self.line1 = self.font.render(
            "You will be shown a number sequence, one number at a time.", 1,
            (0, 0, 0))
        self.screen.blit(self.line1, (100, self.screen_y / 2 - 200))

        self.line2 = self.font.render(
            "Memorize the number sequence.", 1, (0, 0, 0))
        self.screen.blit(self.line2, (100, self.screen_y / 2 - 100))

        self.line3 = self.font.render(
            "You will then be asked to type the sequence in reverse/backwards order. For example...",
            1, (0, 0, 0))
        self.screen.blit(self.line3, (100, self.screen_y / 2))

        self.line4 = self.font.render("Sequence: 1 2 3 4 5", 1,
                                      (0, 0, 0))
        self.line4W = self.line4.get_rect().width
        self.screen.blit(self.line4, (
            self.screen_x / 2 - self.line4W / 2, self.screen_y / 2 + 100))

        self.line5 = self.font.render("Correct: 5 4 3 2 1", 1,
                                      (0, 0, 0))
        self.line5W = self.line5.get_rect().width
        self.screen.blit(self.line5, (
            self.screen_x / 2 - self.line5W / 2, self.screen_y / 2 + 150))

        self.line6 = self.font.render(
            "The sequences will get longer throughout the experiment.", 1,
            (0, 0, 0))
        self.screen.blit(self.line6, (100, self.screen_y / 2 + 250))

        display.text_space(self.screen, self.font,
                           "center", self.screen_y/2 + 350)

        self.instructions = True
        while self.instructions:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.instructions = False
                elif event.type == KEYDOWN and event.key == K_F4:
                    return pd.DataFrame()
                elif event.type == KEYDOWN and event.key == K_F12:
                    pygame.quit()
                    exit()

            pygame.display.flip()

        # Instructions Practice
        self.instructionsPractice = True
        while self.instructionsPractice:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.instructionsPractice = False
                elif event.type == KEYDOWN and event.key == K_F4:
                    return pd.DataFrame()
                elif event.type == KEYDOWN and event.key == K_F12:
                    pygame.quit()
                    exit()

                self.screen.blit(self.background, (0, 0))
                self.practiceInstructions = self.font.render(
                    "We will begin with a practice trial...", 1, (0, 0, 0))
                self.screen.blit(self.practiceInstructions,
                                 (100, self.screen_y / 2))

                display.text_space(self.screen, self.font,
                                   "center", self.screen_y/2 + 100)

                pygame.display.flip()

        # Practice trial
        self.practiceData = pd.DataFrame(['13579'], columns=['sequence'])
        self.correctSequence_p = self.display_numbers(0, self.practiceData)
        self.userSequence_p = self.number_entry()

        # Practice feedback screen
        self.screen.blit(self.background, (0, 0))

        if list(reversed(self.correctSequence_p)) == self.userSequence_p:
            self.feedbackLine = self.font.render("Correct", 1,
                                                 (0, 255, 0))
        else:
            self.feedbackLine = self.font.render("Incorrect", 1,
                                                 (255, 0, 0))

        self.feedbackLineH = self.feedbackLine.get_rect().height
        self.feedbackLineW = self.feedbackLine.get_rect().width

        self.screen.blit(self.feedbackLine, (
            self.screen_x / 2 - self.feedbackLineW / 2,
            self.screen_y / 2 - self.feedbackLineH / 2))

        pygame.display.flip()

        self.baseTime = int(round(time.time() * 1000))
        while int(round(time.time() * 1000)) - self.baseTime < 2000:
            pass

        # Practice end screen
        self.practiceEndScreen = True
        while self.practiceEndScreen:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.practiceEndScreen = False

            self.screen.blit(self.background, (0, 0))
            self.practiceEndLine = self.font.render(
                "We will now begin the main trials...", 1, (0, 0, 0))
            self.screen.blit(self.practiceEndLine, (100, self.screen_y / 2))

            display.text_space(self.screen, self.font,
                               "center", self.screen_y/2 + 100)

            pygame.display.flip()

        # Main trials
        for i in range(self.all_data.shape[0]):
            self.correctSequence = self.display_numbers(i, self.all_data)
            self.user_sequence = self.number_entry()

            self.all_data.set_value(i, 'user_sequence',
                                   ''.join(self.user_sequence))

            if len(self.correctSequence) != len(self.user_sequence):
                self.all_data.set_value(i, 'correct', 0)
            else:
                if list(reversed(self.correctSequence)) == self.user_sequence:
                    self.all_data.set_value(i, 'correct', 1)
                else:
                    self.all_data.set_value(i, 'correct', 0)

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
                               "center", self.screen_y/2 + 100)

            pygame.display.flip()

        print "- Digit span (backwards) complete"

        return self.all_data
