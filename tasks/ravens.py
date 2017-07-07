import time
import pandas as pd
import numpy as np
import pygame

from pygame.locals import *
from os import listdir
from os.path import join, dirname, realpath, splitext
from sys import exit


class Ravens(object):
    def __init__(self, screen, background, start=13, numTrials=12):
        # Get the pygame display window
        self.screen = screen
        self.background = background

        # sets font and font size
        self.instructionsFont = pygame.font.SysFont("arial", 20)

        # get screen info
        self.screen_x = self.screen.get_width()
        self.screen_y = self.screen.get_height()

        # Fill background
        self.background.fill((255, 255, 255))
        pygame.display.set_caption("Ravens Progressive Matrices")
        pygame.mouse.set_visible(0)

        # set number of trials
        self.numTrials = numTrials
        self.stimDuration = 60000
        self.ITI = 1000

        # get images
        self.directory = dirname(realpath(__file__))
        self.imagePath = self.directory + "\images\\Ravens\\"

        # store all filenames in the images path to a list
        self.dirImages = [f for f in listdir(self.imagePath) if
                          splitext(join(self.imagePath, f))[-1] == '.png']
        
        self.dirImages = sorted(self.dirImages)

        # only load the desired number/set of images
        self.images = []
        for i in range(start - 1, start + numTrials - 1):
            self.images.append(
                pygame.image.load(self.imagePath + self.dirImages[i]))

        # get image size
        self.stimH = self.images[0].get_rect().height
        self.stimW = self.images[0].get_rect().width

        # load practice image
        self.practiceImage = pygame.image.load(
            self.imagePath + "practice\\practice.png")

        # load instructions page example images
        self.img_example = pygame.image.load(
            self.imagePath + "practice\\example.png")
        self.exampleW = self.img_example.get_rect().width

        self.img_example_answers = pygame.image.load(
            self.imagePath + "practice\\example_answers.png")
        self.exampleAnswersW = self.img_example_answers.get_rect().width

        # ravens set 2 answers
        self.correctAnswers = np.array([
            5,  # 1
            1,  # 2
            7,  # 3
            4,  # 4
            3,  # 5
            1,  # 6
            6,  # 7
            1,  # 8
            8,  # 9
            4,  # 10
            5,  # 11
            6,  # 12
            2,  # 13
            1,  # 14
            2,  # 15
            4,  # 16
            6,  # 17
            7,  # 18
            3,  # 19
            8,  # 20
            8,  # 21
            7,  # 22
            6,  # 23
            3,  # 24
            7,  # 25
            2,  # 26
            7,  # 27
            5,  # 28
            6,  # 29
            5,  # 30
            4,  # 31
            8,  # 32
            5,  # 33
            1,  # 34
            3,  # 35
            2,  # 36
        ])

        # create output dataframe
        self.allData = pd.DataFrame()
        self.trial = np.arange(1, numTrials + 1)
        self.allData['trial'] = self.trial
        self.stimNum = np.arange(start, start + numTrials)
        self.allData['image'] = self.stimNum
        self.answerSubset = self.correctAnswers[
                            start - 1:start + numTrials - 1]
        self.allData['correctAnswer'] = self.answerSubset

    def pressSpace(self, x, y):
        self.space = self.instructionsFont.render(
            "(Press spacebar when ready)", 1, (0, 0, 0))
        self.screen.blit(self.space, (x, y))

    def displayTrial(self, i, data, type):
        # clear the event queue before checking for responses
        pygame.event.clear()

        if type == "main":
            self.curImage = self.images[i]
        elif type == "practice":
            self.curImage = self.practiceImage

        self.baseTime = int(round(time.time() * 1000))
        while int(
                round(time.time() * 1000)) - self.baseTime < self.stimDuration:
            self.endTime = int(round(time.time() * 1000))

            data.set_value(i, 'userAnswer', "NA")
            data.set_value(i, 'RT', "NA")

            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_F12:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_1:
                        data.set_value(i, 'userAnswer', '1')
                        data.set_value(i, 'RT', str((float(
                            self.endTime) - float(self.baseTime)) / 1000))
                        return 0
                    elif event.key == K_2:
                        data.set_value(i, 'userAnswer', '2')
                        data.set_value(i, 'RT', str((float(
                            self.endTime) - float(self.baseTime)) / 1000))
                        return 0
                    elif event.key == K_3:
                        data.set_value(i, 'userAnswer', '3')
                        data.set_value(i, 'RT', str((float(
                            self.endTime) - float(self.baseTime)) / 1000))
                        return 0
                    elif event.key == K_4:
                        data.set_value(i, 'userAnswer', '4')
                        data.set_value(i, 'RT', str((float(
                            self.endTime) - float(self.baseTime)) / 1000))
                        return 0
                    elif event.key == K_5:
                        data.set_value(i, 'userAnswer', '5')
                        data.set_value(i, 'RT', str((float(
                            self.endTime) - float(self.baseTime)) / 1000))
                        return 0
                    elif event.key == K_6:
                        data.set_value(i, 'userAnswer', '6')
                        data.set_value(i, 'RT', str((float(
                            self.endTime) - float(self.baseTime)) / 1000))
                        return 0
                    elif event.key == K_7:
                        data.set_value(i, 'userAnswer', '7')
                        data.set_value(i, 'RT', str((float(
                            self.endTime) - float(self.baseTime)) / 1000))
                        return 0
                    elif event.key == K_8:
                        data.set_value(i, 'userAnswer', '8')
                        data.set_value(i, 'RT', str((float(
                            self.endTime) - float(self.baseTime)) / 1000))
                        return 0

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.curImage, (
                self.screen_x / 2 - self.stimW / 2,
                self.screen_y / 2 - self.stimH / 2))

            self.timeLeft = self.stimDuration / 1000 - (self.endTime - self.baseTime) / 1000
            # convert seconds to time format
            self.timer = time.strftime('%M:%S', time.gmtime(self.timeLeft))

            self.timerText = self.instructionsFont.render(
                "Time left: " + str(self.timer), 1, (0, 0, 0))
            self.timerW = self.timerText.get_rect().width
            self.screen.blit(self.timerText, (
                self.screen_x / 2 - self.timerW / 2, self.screen_y / 2 + 400))

            pygame.display.flip()

    def run(self):
        # Instructions
        self.screen.blit(self.background, (0, 0))

        self.title = self.instructionsFont.render(
            "Raven's Progressive Matrices", 1, (0, 0, 0))
        self.titleW = self.title.get_rect().width
        self.screen.blit(self.title, (
            self.screen_x / 2 - self.titleW / 2, self.screen_y / 2 - 400))

        self.line1 = self.instructionsFont.render(
            "You will see a grid of items with one item missing:", 1,
            (0, 0, 0))
        self.screen.blit(self.line1, (100, self.screen_y / 2 - 350))

        self.screen.blit(self.img_example, (
            self.screen_x / 2 - self.exampleW / 2, self.screen_y / 2 - 300))

        self.line2 = self.instructionsFont.render(
            "There will be a set of 8 possible answer options:", 1, (0, 0, 0))
        self.screen.blit(self.line2, (100, self.screen_y / 2 - 100))

        self.screen.blit(self.img_example_answers, (
            self.screen_x / 2 - self.exampleAnswersW / 2,
            self.screen_y / 2 - 50))

        self.line3 = self.instructionsFont.render(
            "Determine which option is the missing item.", 1, (0, 0, 0))
        self.screen.blit(self.line3, (100, self.screen_y / 2 + 150))

        self.line4 = self.instructionsFont.render(
            "In example above, the correct answer is 4.", 1, (0, 0, 0))
        self.screen.blit(self.line4, (100, self.screen_y / 2 + 180))

        self.line5 = self.instructionsFont.render(
            "Select your answer by pressing the corresponding number on the keyboard.",
            1, (0, 0, 0))
        self.screen.blit(self.line5, (100, self.screen_y / 2 + 250))

        self.line6 = self.instructionsFont.render(
            "You will have 1 minute to complete each question.", 1, (0, 0, 0))
        self.screen.blit(self.line6, (100, self.screen_y / 2 + 280))

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

        # Practice trials
        self.practiceData = pd.DataFrame()
        self.displayTrial(0, self.practiceData, "practice")

        # Practice feedback screen
        self.screen.blit(self.background, (0, 0))

        if self.practiceData.at[0, 'userAnswer'] == '2':
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

        # show feedback screen for 2 seconds
        self.baseTime = int(round(time.time() * 1000))
        while int(round(time.time() * 1000)) - self.baseTime < 2000:
            pass

        # Instructions Practice End
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

        # Main task
        for i in range(self.numTrials):
            self.displayTrial(i, self.allData, "main")

            if self.allData.at[i, 'userAnswer'] == str(
                    self.allData.at[i, 'correctAnswer']):
                self.allData.set_value(i, 'correct', 1)
            else:
                self.allData.set_value(i, 'correct', 0)

            self.baseTime = int(round(time.time() * 1000))
            while int(round(time.time() * 1000)) - self.baseTime < self.ITI:
                self.screen.blit(self.background, (0, 0))
                pygame.display.flip()

        # rearrange dataframe
        self.columns = ['trial', 'image', 'correctAnswer', 'userAnswer',
                        'correct', 'RT']
        self.allData = self.allData[self.columns]

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

        print("- Raven's Progressive Matrices complete")

        return self.allData
