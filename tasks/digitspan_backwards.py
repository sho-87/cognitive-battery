import sys
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

        # Get screen info
        self.screen_x = self.screen.get_width()
        self.screen_y = self.screen.get_height()

        # Fill background
        self.background.fill((255, 255, 255))
        pygame.display.set_caption("Backwards Digitspan")
        pygame.mouse.set_visible(0)

        # Experiment options
        self.STIM_DURATION = 1000  # Duration of each digit
        self.INTER_NUMBER_DURATION = 100  # Time between numbers
        self.FEEDBACK_DURATION = 2000  # Duration of feedback screen
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

    def check_answer(self, user_string, actual_string):
        if user_string[::-1] == actual_string:
            return True
        else:
            return False

    def run(self):
        # Instructions
        self.screen.blit(self.background, (0, 0))

        display.text(self.screen, self.font, "Backwards Digit Span",
                     "center", self.screen_y/2 - 300)

        display.text(self.screen, self.font,
                     "You will be shown a number sequence, "
                     "one number at a time",
                     100, self.screen_y/2 - 200)

        display.text(self.screen, self.font,
                     "Memorize the number sequence",
                     100, self.screen_y/2 - 100)

        display.text(self.screen, self.font,
                     "You will then be asked to type the sequence "
                     "in reverse/backwards order. For example...",
                     100, "center")

        display.text(self.screen, self.font,
                     "Sequence: 1 2 3 4 5",
                     "center", self.screen_y/2 + 100)

        display.text(self.screen, self.font,
                     "Correct: 5 4 3 2 1",
                     "center", self.screen_y/2 + 150)

        display.text(self.screen, self.font,
                     "The sequences will get longer throughout the experiment",
                     100, self.screen_y/2 + 250)

        display.text_space(self.screen, self.font,
                           "center", self.screen_y/2 + 350)

        pygame.display.flip()

        display.wait_for_space()

        # Instructions Practice
        self.screen.blit(self.background, (0, 0))

        display.text(self.screen, self.font,
                     "We will begin with a practice trial...",
                     100, "center")

        display.text_space(self.screen, self.font,
                           "center", self.screen_y/2 + 100)

        pygame.display.flip()

        display.wait_for_space()

        # Practice trial
        practice_data = pd.DataFrame(['13579'], columns=['sequence'])
        correct_sequence_p = self.display_numbers(0, practice_data)
        user_sequence_p = self.number_entry()

        # Practice feedback screen
        self.screen.blit(self.background, (0, 0))

        # Check if reverse of user input matches the correct sequence
        if self.check_answer(user_sequence_p, correct_sequence_p):
            display.text(self.screen, self.font, "Correct",
                         "center", "center", (0, 255, 0))
        else:
            display.text(self.screen, self.font, "Incorrect",
                         "center", "center", (255, 0, 0))

        pygame.display.flip()

        display.wait(self.FEEDBACK_DURATION)

        # Practice end screen
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font,
                     "We will now begin the main trials...", 100, "center")
        display.text_space(self.screen, self.font,
                           "center", self.screen_y/2 + 100)

        pygame.display.flip()

        display.wait_for_space()

        # Main trials
        for i in range(len(self.all_data)):
            correct_sequence = self.display_numbers(i, self.all_data)
            user_sequence = self.number_entry()

            self.all_data.set_value(i, 'user_sequence', user_sequence)

            if self.check_answer(user_sequence, correct_sequence):
                self.all_data.set_value(i, 'correct', 1)
            else:
                self.all_data.set_value(i, 'correct', 0)

        # End screen
        self.screen.blit(self.background, (0, 0))
        display.text(self.screen, self.font, "End of task", "center", "center")
        display.text_space(self.screen, self.font,
                           "center", self.screen_y/2 + 100)

        pygame.display.flip()

        display.wait_for_space()

        print("- Digit span (backwards) complete")

        return self.all_data
