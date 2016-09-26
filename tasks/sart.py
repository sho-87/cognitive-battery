import os
import time
import pandas as pd
import numpy as np
import pygame

from pygame.locals import *
from sys import exit


class SART(object):
    def __init__(self, screen):
        # Get the pygame display window
        self.screen = screen

        # sets font and font size
        self.instructionsFont = pygame.font.SysFont("arial", 30)

        # get screen info
        self.screen_x = self.screen.get_width()
        self.screen_y = self.screen.get_height()

        # fills background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        pygame.display.set_caption("SART Task")
        pygame.mouse.set_visible(0)

        # get mask image
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.imagePath = self.directory + "\images\\SART\\"
        # this uses the 29mm mask image (as described by Robertson 1997)
        self.maskImage = pygame.image.load(self.imagePath + 'mask_29.png')
        self.maskX, self.maskY = self.maskImage.get_rect().size

        # set variables
        self.stimDuration = 0.25
        self.ITI = 0.9
        self.stimSizes_pt = [48, 72, 94, 100,
                             120]  # in point as per original paper
        self.stimSizes_mm = [12, 18, 23, 24,
                             29]  # in mm, maintaining original ratio

        # create trial sequence
        self.numberSet = np.repeat(np.arange(1, 10), 25)
        np.random.shuffle(self.numberSet)
        self.trialNum = np.arange(1, 226)

        # create output dataframe
        self.allData = pd.DataFrame()
        self.allData["trial"] = self.trialNum
        self.allData["stimulus"] = self.numberSet

    def pressSpace(self, x, y):
        self.space = self.instructionsFont.render(
            "(Press spacebar when ready)", 1, (255, 255, 255))
        self.screen.blit(self.space, (x, y))

    def displayTrial(self, i, data):
        # randomly choose font size
        self.sizeIndex = np.random.randint(0, 5)
        self.stimulusFont = pygame.font.SysFont("arial", self.stimSizes_pt[
            self.sizeIndex])

        # set stimulus
        self.stimulusText = self.stimulusFont.render(
            str(data.at[i, "stimulus"]), 1, (255, 255, 255))
        self.stimulusH = self.stimulusText.get_rect().height
        self.stimulusW = self.stimulusText.get_rect().width

        self.keyPress = 0
        data.set_value(i, 'RT', 1150)

        # get start time in ms
        self.baseTime = int(round(time.time() * 1000))

        pygame.event.clear()
        # keep trial to under 1150ms
        while int(round(time.time() * 1000)) - self.baseTime <= 1150:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.keyPress = 1
                    data.set_value(i, 'RT', int(
                        round(time.time() * 1000)) - self.baseTime)
                elif event.type == KEYDOWN and event.key == K_F4:
                    return pd.DataFrame()
                elif event.type == KEYDOWN and event.key == K_F12:
                    pygame.quit()
                    exit()

            self.screen.blit(self.background, (0, 0))

            # display stim for 250ms
            if int(round(time.time() * 1000)) - self.baseTime <= 250:
                self.screen.blit(self.stimulusText, (
                    self.screen_x / 2 - self.stimulusW / 2,
                    self.screen_y / 2 - self.stimulusH / 2))
            else:
                # display post stim mask for 900ms
                self.screen.blit(self.maskImage, (
                    [self.screen_x / 2 - self.maskX / 2,
                     self.screen_y / 2 - self.maskY / 2],
                    [self.screen_x / 2 + self.maskX / 2,
                     self.screen_y / 2 + self.maskY / 2]))

            pygame.display.flip()

        # check if response is correct
        if data.at[i, "stimulus"] == 3:
            if self.keyPress == 0:
                self.accuracy = 1
            else:
                self.accuracy = 0
        else:
            if self.keyPress == 0:
                self.accuracy = 0
            else:
                self.accuracy = 1

        # store key press data in dataframe
        data.set_value(i, 'key press', self.keyPress)
        data.set_value(i, 'accuracy', self.accuracy)
        data.set_value(i, 'stimSize', self.stimSizes_pt[self.sizeIndex])

    def run(self):
        # Instructions
        self.screen.blit(self.background, (0, 0))

        self.title = self.instructionsFont.render("SART", 1, (255, 255, 255))
        self.titleW = self.title.get_rect().width
        self.screen.blit(self.title, (
            self.screen_x / 2 - self.titleW / 2, self.screen_y / 2 - 250))

        self.line1 = self.instructionsFont.render(
            "Numbers will appear in the center of the screen.", 1,
            (255, 255, 255))
        self.screen.blit(self.line1, (100, self.screen_y / 2 - 100))

        self.line2 = self.instructionsFont.render(
            "Press the spacebar after you see a number.", 1, (255, 255, 255))
        self.screen.blit(self.line2, (100, self.screen_y / 2))

        self.line3 = self.instructionsFont.render(
            "However, if the number is a 3, do NOT press the spacebar.", 1,
            (255, 255, 255))
        self.screen.blit(self.line3, (100, self.screen_y / 2 + 100))

        self.pressSpace(100, (self.screen_y / 2) + 250)

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
                    "We will begin with a few practice trials...", 1,
                    (255, 255, 255))
                self.screen.blit(self.practiceInstructions,
                                 (100, self.screen_y / 2))

                self.pressSpace(100, (self.screen_y / 2) + 100)

                pygame.display.flip()

        # Practice trials
        self.practiceTrials = pd.DataFrame([5, 7, 7, 3, 9, 2, 1, 3, 8, 6],
                                           columns=['stimulus'])

        for i in range(self.practiceTrials.shape[0]):
            self.displayTrial(i, self.practiceTrials)

        # Practice end screen
        self.practiceEndScreen = True
        while self.practiceEndScreen:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.practiceEndScreen = False

            self.screen.blit(self.background, (0, 0))
            self.practiceEndLine = self.instructionsFont.render(
                "We will now begin the main trials...", 1, (255, 255, 255))
            self.screen.blit(self.practiceEndLine, (100, self.screen_y / 2))

            self.pressSpace(100, (self.screen_y / 2) + 100)

            pygame.display.flip()

        # Main trials
        for i in range(self.allData.shape[0]):
            self.displayTrial(i, self.allData)

        # rearrange dataframe
        columns = ['trial', 'stimulus', 'stimSize', 'RT', 'key press',
                   'accuracy']
        self.allData = self.allData[columns]

        # End screen
        self.endScreen = True
        while self.endScreen:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.endScreen = False

            self.screen.blit(self.background, (0, 0))
            self.endLine = self.instructionsFont.render("End of task.", 1,
                                                        (255, 255, 255))
            self.screen.blit(self.endLine, (100, self.screen_y / 2))

            self.pressSpace(100, (self.screen_y / 2) + 100)

            pygame.display.flip()

        print "- SART complete"

        return self.allData
