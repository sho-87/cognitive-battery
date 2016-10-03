import time
import pandas as pd
import numpy as np
import pygame

from pygame.locals import *
from sys import exit


class DigitspanBackwards(object):
    def __init__(self, screen, background):
        # Get the pygame display window
        self.screen = screen
        self.background = background

        # sets font and font size
        self.instructionsFont = pygame.font.SysFont("arial", 30)
        self.stimulusFont = pygame.font.SysFont("arial", 80)

        # get screen info
        self.screen_x = self.screen.get_width()
        self.screen_y = self.screen.get_height()

        # Fill background
        self.background.fill((255, 255, 255))
        pygame.display.set_caption("Backwards Digitspan")
        pygame.mouse.set_visible(0)

        # set stimulus timings
        self.stimDuration = 1000
        self.ITI = 100

        # create digit lengths
        self.startLength = 3
        self.endLength = 9
        self.numLengths = self.endLength - self.startLength + 1
        self.numRepetitions = 2
        self.trialNum = np.arange(1, self.numLengths * self.numRepetitions + 1)

        self.digitLengths = np.asarray(
            [j for i in range(self.startLength, self.endLength + 1) for j in
             [i, i]])

        # main dataframe
        self.allData = pd.DataFrame()
        self.allData["trial"] = self.trialNum
        self.allData["length"] = self.digitLengths

        # create digit sequences
        for i in range(self.allData.shape[0]):
            # set initial empty sequence
            self.generatedSequence = ''
            for j in range(self.allData.at[i, 'length']):
                # generate initial random number
                self.randomNum = str(np.random.randint(1, 10))
                # if that number is in the sequence, generate new number
                while self.randomNum in [c for c in self.generatedSequence]:
                    self.randomNum = str(np.random.randint(1, 10))
                # add number to the sequence
                self.generatedSequence += self.randomNum
            # add sequence to dataframe
            self.allData.set_value(i, 'sequence', self.generatedSequence)

    def pressSpace(self, x, y):
        self.space = self.instructionsFont.render(
            "(Press spacebar when ready)", 1, (0, 0, 0))
        self.screen.blit(self.space, (x, y))

    def displayNumbers(self, i, data):
        self.sequence = [c for c in data.at[i, 'sequence']]

        for number in self.sequence:
            self.stimulusText = self.stimulusFont.render(number, 1, (0, 0, 0))
            self.stimulusH = self.stimulusText.get_rect().height
            self.stimulusW = self.stimulusText.get_rect().width

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.stimulusText, (
                self.screen_x / 2 - self.stimulusW / 2,
                self.screen_y / 2 - self.stimulusH / 2))
            pygame.display.flip()

            self.baseTime = int(round(time.time() * 1000))
            while int(
                    round(time.time() * 1000)) - self.baseTime < self.stimDuration:
                pass

            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

            self.baseTime = int(round(time.time() * 1000))
            while int(round(time.time() * 1000)) - self.baseTime < self.ITI:
                pass

        return self.sequence

    def numberEntry(self):
        self.userSequence = []

        # Clear the event queue before checking for responses
        pygame.event.clear()

        self.entry = True
        while self.entry:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.entry = False
                elif event.type == KEYDOWN and event.key == K_F12:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                    if self.userSequence:
                        self.userSequence.pop()
                elif event.type == KEYDOWN:
                    if event.key == K_0:
                        self.userSequence.append(str(0))
                    elif event.key == K_1:
                        self.userSequence.append(str(1))
                    elif event.key == K_2:
                        self.userSequence.append(str(2))
                    elif event.key == K_3:
                        self.userSequence.append(str(3))
                    elif event.key == K_4:
                        self.userSequence.append(str(4))
                    elif event.key == K_5:
                        self.userSequence.append(str(5))
                    elif event.key == K_6:
                        self.userSequence.append(str(6))
                    elif event.key == K_7:
                        self.userSequence.append(str(7))
                    elif event.key == K_8:
                        self.userSequence.append(str(8))
                    elif event.key == K_9:
                        self.userSequence.append(str(9))

            self.screen.blit(self.background, (0, 0))

            self.entryInstructions = self.instructionsFont.render(
                "Type the sequence in backwards order:", 1, (0, 0, 0))

            self.sequenceText = self.stimulusFont.render(
                ''.join(self.userSequence), 1, (0, 0, 0))
            self.sequenceTextH = self.sequenceText.get_rect().height
            self.sequenceTextW = self.sequenceText.get_rect().width

            self.screen.blit(self.entryInstructions, (10, self.screen_y / 4))
            self.screen.blit(self.sequenceText, (
                self.screen_x / 2 - self.sequenceTextW / 2,
                self.screen_y / 2 - self.sequenceTextH / 2))
            pygame.display.flip()

        return self.userSequence

    def run(self):
        # Instructions
        self.screen.blit(self.background, (0, 0))

        self.title = self.instructionsFont.render("Backwards Digit Span", 1,
                                                  (0, 0, 0))
        self.titleW = self.title.get_rect().width
        self.screen.blit(self.title, (
            self.screen_x / 2 - self.titleW / 2, self.screen_y / 2 - 300))

        self.line1 = self.instructionsFont.render(
            "You will be shown a number sequence, one number at a time.", 1,
            (0, 0, 0))
        self.screen.blit(self.line1, (100, self.screen_y / 2 - 200))

        self.line2 = self.instructionsFont.render(
            "Memorize the number sequence.", 1, (0, 0, 0))
        self.screen.blit(self.line2, (100, self.screen_y / 2 - 100))

        self.line3 = self.instructionsFont.render(
            "You will then be asked to type the sequence in reverse/backwards order. For example...",
            1, (0, 0, 0))
        self.screen.blit(self.line3, (100, self.screen_y / 2))

        self.line4 = self.instructionsFont.render("Sequence: 1 2 3 4 5", 1,
                                                  (0, 0, 0))
        self.line4W = self.line4.get_rect().width
        self.screen.blit(self.line4, (
            self.screen_x / 2 - self.line4W / 2, self.screen_y / 2 + 100))

        self.line5 = self.instructionsFont.render("Correct: 5 4 3 2 1", 1,
                                                  (0, 0, 0))
        self.line5W = self.line5.get_rect().width
        self.screen.blit(self.line5, (
            self.screen_x / 2 - self.line5W / 2, self.screen_y / 2 + 150))

        self.line6 = self.instructionsFont.render(
            "The sequences will get longer throughout the experiment.", 1,
            (0, 0, 0))
        self.screen.blit(self.line6, (100, self.screen_y / 2 + 250))

        self.pressSpace(100, (self.screen_y / 2) + 350)

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
                self.practiceInstructions = self.instructionsFont.render(
                    "We will begin with a practice trial...", 1, (0, 0, 0))
                self.screen.blit(self.practiceInstructions,
                                 (100, self.screen_y / 2))

                self.pressSpace(100, (self.screen_y / 2) + 100)

                pygame.display.flip()

        # Practice trial
        self.practiceData = pd.DataFrame(['13579'], columns=['sequence'])
        self.correctSequence_p = self.displayNumbers(0, self.practiceData)
        self.userSequence_p = self.numberEntry()

        # Practice feedback screen
        self.screen.blit(self.background, (0, 0))

        if list(reversed(self.correctSequence_p)) == self.userSequence_p:
            self.feedbackLine = self.instructionsFont.render("Correct", 1,
                                                             (0, 255, 0))
        else:
            self.feedbackLine = self.instructionsFont.render("Incorrect", 1,
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
            self.practiceEndLine = self.instructionsFont.render(
                "We will now begin the main trials...", 1, (0, 0, 0))
            self.screen.blit(self.practiceEndLine, (100, self.screen_y / 2))

            self.pressSpace(100, (self.screen_y / 2) + 100)

            pygame.display.flip()

        # Main trials
        for i in range(self.allData.shape[0]):
            self.correctSequence = self.displayNumbers(i, self.allData)
            self.userSequence = self.numberEntry()

            self.allData.set_value(i, 'userSequence',
                                   ''.join(self.userSequence))

            if len(self.correctSequence) != len(self.userSequence):
                self.allData.set_value(i, 'correct', 0)
            else:
                if list(reversed(self.correctSequence)) == self.userSequence:
                    self.allData.set_value(i, 'correct', 1)
                else:
                    self.allData.set_value(i, 'correct', 0)

        # End screen
        self.endScreen = True
        while self.endScreen:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.endScreen = False

            self.screen.blit(self.background, (0, 0))
            self.endLine = self.instructionsFont.render("End of task.", 1,
                                                        (0, 0, 0))
            self.screen.blit(self.endLine, (100, self.screen_y / 2))

            self.pressSpace(100, (self.screen_y / 2) + 100)

            pygame.display.flip()

        print "- Digit span (backwards) complete"

        return self.allData
