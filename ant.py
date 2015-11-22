import pandas as pd
import numpy as np
import pygame
import time
import os
from pygame.locals import *
from itertools import product
from sys import exit

class ANT(object):
    def __init__(self, blocks = 3):
        #initialize pygame
        pygame.init()
        pygame.font.init()

        #sets font and font size
        self.instructionsFont = pygame.font.SysFont("arial", 30)

        #get images
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.imagePath = self.directory + "\images\\ANT\\"

        self.img_left_congruent = pygame.image.load(self.imagePath + 'left_congruent.png')
        self.img_left_incongruent = pygame.image.load(self.imagePath + 'left_incongruent.png')
        self.img_right_congruent = pygame.image.load(self.imagePath + 'right_congruent.png')
        self.img_right_incongruent = pygame.image.load(self.imagePath + 'right_incongruent.png')
        self.img_left_neutral = pygame.image.load(self.imagePath + 'left_neutral.png')
        self.img_right_neutral = pygame.image.load(self.imagePath + 'right_neutral.png')

        self.img_fixation = pygame.image.load(self.imagePath + 'fixation.png')
        self.img_cue = pygame.image.load(self.imagePath + 'cue.png')

        #get image dimensions
        self.flankerW = self.img_left_incongruent.get_rect().width
        self.flankerH = self.img_left_incongruent.get_rect().height
        self.fixationW = self.img_fixation.get_rect().width
        self.fixationH = self.img_fixation.get_rect().height

        #open window
        #self.screen = pygame.display.set_mode((1280, 1024), RESIZABLE)
        self.screen = pygame.display.set_mode((0,0), FULLSCREEN)

        #get screen info
        self.screen_x = self.screen.get_width()
        self.screen_y = self.screen.get_height()

        #fills background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))
        pygame.display.set_caption("ANT Task")
        pygame.mouse.set_visible(0)

        #set number of blocks
        self.numBlocks = blocks

        #Specify factor levels, and task timings as used by Fan et al. (2002).

        self.congruencyLevels = ["congruent", "incongruent", 'neutral']

        self.cueLevels = ["nocue", "center", "spatial", 'double']

        self.locationLevels = ['top', 'bottom']

        self.directionLevels = ['left', 'right']

        self.fixationDurationRange = [400, 1600]

        #Create level combinations
        #level combinations give us 48 trials.
        self.combinations = list(product(self.congruencyLevels, self.cueLevels, self.locationLevels, self.directionLevels))

        #create output dataframe
        self.allData = pd.DataFrame()

    def createBlock(self, blockNum, combinations, type):
        if type == "main":
            curCombinations = combinations*2
            np.random.shuffle(curCombinations)
        elif type == "practice":
            np.random.shuffle(combinations)
            curCombinations = combinations[:len(combinations)/2]

        #add combinations to dataframe
        self.curBlock = pd.DataFrame(data = curCombinations, columns=('congruency', 'cue', 'location', 'direction'))

        #add timing info to dataframe
        self.curBlock["block"] = blockNum+1
        self.curBlock["fixationTime"] = [x for x in np.random.randint(self.fixationDurationRange[0], self.fixationDurationRange[1], len(curCombinations))]

        return self.curBlock

    def pressSpace(self, x, y):
    	self.space = self.instructionsFont.render("(Press spacebar when ready)", 1, (0,0,0))
    	self.screen.blit(self.space, (x, y))

    def displayFlanker(self, trialNum, data, flankerType, location, direction):
        #left
        if direction == "left":
            if flankerType == "congruent":
                self.stimulus = self.img_left_congruent
            elif flankerType == "incongruent":
                self.stimulus = self.img_left_incongruent
            elif flankerType == "neutral":
                self.stimulus = self.img_left_neutral
        #right
        elif direction == "right":
            if flankerType == "congruent":
                self.stimulus = self.img_right_congruent
            elif flankerType == "incongruent":
                self.stimulus = self.img_right_incongruent
            elif flankerType == "neutral":
                self.stimulus = self.img_right_neutral

        #offset the flanker stimulus to above/below fixation
        if location == "top":
            self.screen.blit(self.stimulus, (self.screen_x/2 - self.flankerW/2, self.screen_y/2 - self.flankerH - 31))
        elif location == "bottom":
            self.screen.blit(self.stimulus, (self.screen_x/2 - self.flankerW/2, self.screen_y/2 + 31))

    def displayTrial(self, trialNum, data, type):
        #check for a quit press after stimulus was shown
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_F4:
                return pd.DataFrame()
            elif event.type == KEYDOWN and event.key == K_F12:
                pygame.quit()
                exit()

        #display fixation period
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.img_fixation, (self.screen_x/2 - self.fixationW/2, self.screen_y/2 - self.fixationH/2))
        pygame.display.flip()

        self.baseTime = int(round(time.time() * 1000))
        while int(round(time.time() * 1000)) - self.baseTime < data.at[trialNum, "fixationTime"]:
            pass

        #cues
        self.screen.blit(self.background, (0,0))
        if data.at[trialNum, "cue"] == "nocue":
            self.screen.blit(self.img_fixation, (self.screen_x/2 - self.fixationW/2, self.screen_y/2 - self.fixationH/2))
        elif data.at[trialNum, "cue"] == "center":
            self.screen.blit(self.img_cue, (self.screen_x/2 - self.fixationW/2, self.screen_y/2 - self.fixationH/2))
        elif data.at[trialNum, "cue"] == "double":
            self.screen.blit(self.img_fixation, (self.screen_x/2 - self.fixationW/2, self.screen_y/2 - self.fixationH/2))
            self.screen.blit(self.img_cue, (self.screen_x/2 - self.fixationW/2, self.screen_y/2 - self.fixationH - 31))
            self.screen.blit(self.img_cue, (self.screen_x/2 - self.fixationW/2, self.screen_y/2 + 31))
        elif data.at[trialNum, "cue"] == "spatial":
            self.screen.blit(self.img_fixation, (self.screen_x/2 - self.fixationW/2, self.screen_y/2 - self.fixationH/2))
            if data.at[trialNum, "location"] == "top":
                self.screen.blit(self.img_cue, (self.screen_x/2 - self.fixationW/2, self.screen_y/2 - self.fixationH - 31))
            elif data.at[trialNum, "location"] == "bottom":
                self.screen.blit(self.img_cue, (self.screen_x/2 - self.fixationW/2, self.screen_y/2 + 31))

        pygame.display.flip()

        #display cue for 100ms
        self.baseTime = int(round(time.time() * 1000))
        while int(round(time.time() * 1000)) - self.baseTime < 100:
            pass

        #prestim interval (400ms)
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.img_fixation, (self.screen_x/2 - self.fixationW/2, self.screen_y/2 - self.fixationH/2))

        pygame.display.flip()

        self.baseTime = int(round(time.time() * 1000))
        while int(round(time.time() * 1000)) - self.baseTime < 400:
            pass

        #display target
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.img_fixation, (self.screen_x/2 - self.fixationW/2, self.screen_y/2 - self.fixationH/2))

        self.displayFlanker(trialNum, data, data.at[trialNum, "congruency"], data.at[trialNum, "location"], data.at[trialNum, "direction"])

        pygame.display.flip()

        self.baseTime = int(round(time.time() * 1000))
        self.endTime = self.baseTime

        #clear the event queue before checking for responses
        pygame.event.clear()
        self.waitResponse = True
        while self.waitResponse:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_LEFT:
                    self.response = "left"
                    self.waitResponse = False
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    self.response = "right"
                    self.waitResponse = False
                elif event.type == KEYDOWN and event.key == K_F4:
                    return pd.DataFrame()

            self.endTime = int(round(time.time() * 1000))

            #if time limit has been reached, consider it a missed trial
            if self.endTime - self.baseTime >= 1700:
                self.response = "NA"
                self.waitResponse = False

        self.rt = int(round(time.time() * 1000)) - self.baseTime

        data.set_value(trialNum, 'response', self.response)
        data.set_value(trialNum, 'RT', self.rt)

        if self.response == data.at[trialNum, "direction"]:
            self.correct = 1
        else:
            self.correct = 0

        data.set_value(trialNum, 'correct', self.correct)

        #if practice, display feedback
        if type == "practice":
            self.screen.blit(self.background, (0,0))
            if self.correct == 1:
                self.feedback = self.instructionsFont.render("correct", 1, (0,255,0))
            elif self.correct == 0:
                self.feedback = self.instructionsFont.render("incorrect", 1, (255,0,0))

            self.feedbackW = self.feedback.get_rect().width
            self.feedbackH = self.feedback.get_rect().height
            self.screen.blit(self.feedback, (self.screen_x/2 - self.feedbackW/2, self.screen_y/2 - self.feedbackH/2))

            pygame.display.flip()

            self.baseTime = int(round(time.time() * 1000))
            while int(round(time.time() * 1000)) - self.baseTime < 1000:
                pass

        #ITI
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.img_fixation, (self.screen_x/2 - self.fixationW/2, self.screen_y/2 - self.fixationH/2))

        pygame.display.flip()

        self.ITI = 3500 - self.rt - data.at[trialNum, 'fixationTime']
        data.set_value(trialNum, 'ITI', self.ITI)

        self.baseTime = int(round(time.time() * 1000))
        while int(round(time.time() * 1000)) - self.baseTime < self.ITI:
            pass

    def runBlock(self, blockNum, totalBlocks, type):
        self.curBlock = self.createBlock(blockNum, self.combinations, type)

        for j in range(self.curBlock.shape[0]):
            self.displayTrial(j, self.curBlock, type)

        if type == "main":
            #add block data to allData
            self.allData = pd.concat([self.allData, self.curBlock])

        #end of block screen
        if blockNum != totalBlocks - 1:
            self.blockEnd = True
            while self.blockEnd:
                for event in pygame.event.get():
            		if event.type == KEYDOWN and event.key == K_SPACE:
            			self.blockEnd = False

                self.screen.blit(self.background, (0,0))

                self.blockText = self.instructionsFont.render("End of current block. Start next block when you're ready...", 1, (0,0,0))
                self.screen.blit(self.blockText, (100, self.screen_y/2))

                self.pressSpace(100, (self.screen_y/2) + 100)

                pygame.display.flip()

    def run(self):
        #Instructions
        self.screen.blit(self.background, (0,0))

        self.title = self.instructionsFont.render("Attentional Network Test", 1, (0,0,0))
        self.titleW = self.title.get_rect().width
        self.screen.blit(self.title, (self.screen_x/2 - self.titleW/2, self.screen_y/2 - 300))

        self.line1 = self.instructionsFont.render("Keep your eyes on the fixation cross at the start of each trial:", 1, (0,0,0))
        self.screen.blit(self.line1, (100, self.screen_y/2 - 200))

        self.screen.blit(self.img_fixation, (self.screen_x/2 - self.fixationW/2, self.screen_y/2 - 150))

        self.line2 = self.instructionsFont.render("Then, a set of arrows will appear somewhere on the screen:", 1, (0,0,0))
        self.screen.blit(self.line2, (100, self.screen_y/2 - 100))

        self.screen.blit(self.img_left_incongruent, (self.screen_x/2 - self.flankerW/2, self.screen_y/2 - 50))

        self.line3 = self.instructionsFont.render("Use the left/right arrow keys to indicate the direction of the CENTER arrow only.", 1, (0,0,0))
        self.screen.blit(self.line3, (100, self.screen_y/2))

        self.line4 = self.instructionsFont.render("In example above, the correct answer is LEFT.", 1, (0,0,0))
        self.screen.blit(self.line4, (100, self.screen_y/2 + 50))

        self.pressSpace(100, (self.screen_y/2)+300)

        self.instructions = True
        while self.instructions:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.instructions = False
                elif event.type == KEYDOWN and event.key == K_F12:
                    pygame.quit()
                    exit()

            pygame.display.flip()

        #Instructions Practice
        self.instructionsPractice = True
        while self.instructionsPractice:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.instructionsPractice = False
                elif event.type == KEYDOWN and event.key == K_F12:
                    pygame.quit()
                    exit()

        	self.screen.blit(self.background, (0,0))
        	self.practiceInstructions = self.instructionsFont.render("We will begin with a few practice trials...", 1, (0,0,0))
        	self.screen.blit(self.practiceInstructions, (100, self.screen_y/2))

        	self.pressSpace(100, (self.screen_y/2)+100)

        	pygame.display.flip()

        #Practice trials
        for i in range(1):
            self.runBlock(i, 1, "practice")

        #Instructions Practice End
        self.practiceEndScreen = True
        while self.practiceEndScreen:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.practiceEndScreen = False

            self.screen.blit(self.background, (0,0))
            self.practiceEndLine = self.instructionsFont.render("We will now begin the main trials...", 1, (0,0,0))
            self.screen.blit(self.practiceEndLine, (100, self.screen_y/2 - 50))

            self.practiceEndLine2 = self.instructionsFont.render("You will not receive feedback after each trial.", 1, (0,0,0))
            self.screen.blit(self.practiceEndLine2, (100, self.screen_y/2 + 50))

            self.pressSpace(100, (self.screen_y/2)+200)

            pygame.display.flip()

        #Main task
        for i in range(self.numBlocks):
            self.runBlock(i, self.numBlocks, "main")

        #create trial number column
        self.trialNums = np.arange(1, self.allData.shape[0]+1)
        self.allData["trial"] = self.trialNums

        #rearrange the dataframe
        self.columns = ['trial', 'block', 'congruency', 'cue', 'location', 'fixationTime', 'ITI', 'direction', 'response', 'correct', 'RT']
        self.allData = self.allData[self.columns]

        #End screen
        self.endScreen = True
        while self.endScreen:
        	for event in pygame.event.get():
        		if event.type == KEYDOWN and event.key == K_SPACE:
        			self.endScreen = False

        	self.screen.blit(self.background, (0,0))
        	self.endLine = self.instructionsFont.render("End of task.", 1, (0,0,0))
        	self.screen.blit(self.endLine, (100, self.screen_y/2))

        	self.pressSpace(100, (self.screen_y/2)+100)

        	pygame.display.flip()

        #pygame.quit()

        return self.allData
