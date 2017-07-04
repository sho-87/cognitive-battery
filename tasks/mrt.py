import os
import time
import pandas as pd
import numpy as np
import pygame

from pygame.locals import *
from sys import exit


class MRT(object):
    def __init__(self, screen, background):
        # Get the pygame display window
        self.screen = screen
        self.background = background

        # sets font and font size
        self.xFont = pygame.font.SysFont("arial", 20)

        # get self.screen info
        self.screen_x = self.screen.get_width()
        self.screen_y = self.screen.get_height()
        self.button = (self.screen_x - 1024) / 2

        # Fill background
        self.background.fill((255, 255, 255))
        pygame.display.set_caption("Mental Rotation Task")
        pygame.mouse.set_visible(1)

        # create dataframe for all data
        self.allData = pd.DataFrame([
            [1, 3],  # 1
            [1, 4],  # 2
            [2, 4],  # 3
            [2, 3],  # 4
            [1, 3],  # 5
            [1, 4],  # 6
            [2, 4],  # 7
            [2, 3],  # 8
            [2, 4],  # 9
            [1, 4],  # 10
            [3, 4],  # 11
            [2, 3],  # 12
            [1, 2],  # 13
            [2, 4],  # 14
            [2, 3],  # 15
            [1, 4],  # 16
            [2, 4],  # 17
            [2, 3],  # 18
            [1, 3],  # 19
            [1, 4],  # 20
            [2, 4],  # 21
            [2, 3],  # 22
            [1, 4],  # 23
            [1, 3]  # 24
        ], columns=['correct_answer1', 'correct_answer2'])

        # add blank user answers
        self.allData["user_answer1"] = 0
        self.allData["user_answer2"] = 0

        # add trial numbers
        self.trialNums = np.arange(1, self.allData.shape[0] + 1)
        self.allData["trial"] = self.trialNums

        # temporary storage for practice questions/answers
        self.practiceAnswers = []
        for i in range(3):
            self.practiceAnswers.append([0, 0])

        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.imagePath = self.directory + "\images\\MRT\\"

    def pressSpace(self, x, y):
        self.space = self.xFont.render("(Press spacebar when ready)", 1,
                                       (0, 0, 0))
        self.screen.blit(self.space, (x, y))

    def mainExperiment(self, section, data):
        main = True
        # check for first half or second half to determine current trial number
        if section == 1:
            self.curTrial = 1
        elif section == 2:
            self.curTrial = 13

        # time at task start
        self.start_time = int(time.time())

        while main:
            self.screen.blit(self.background, (0, 0))
            # calculate amount of time left in the task
            self.curTime = int(time.time()) - self.start_time
            self.timeLeft = 180 - self.curTime
            # convert seconds to time format
            self.timer = time.strftime('%M:%S', time.gmtime(self.timeLeft))

            # change timer to red if below 10 seconds remaining (flashing), and every minute
            if self.timeLeft % 60 == 0:
                self.timerColour = (255, 0, 0)
            elif self.timeLeft <= 10:
                if self.timeLeft % 2 == 0:
                    self.timerColour = (255, 0, 0)
                else:
                    self.timerColour = (0, 0, 0)
            else:
                self.timerColour = (0, 0, 0)

            # display the timer
            self.timerText = self.xFont.render("Time left: " + str(self.timer),
                                               1, self.timerColour)
            self.timerW = self.timerText.get_rect().width
            self.screen.blit(self.timerText, (
                self.screen_x / 2 - self.timerW / 2, self.screen_y / 2 + 300))
            # stop if timer hits 0
            if self.timeLeft <= 0:
                main = False

            # draw circles
            if section == 1:
                self.trialOffset = 0
            elif section == 2:
                self.trialOffset = 12

            for i in range(12):
                # draws indicating arrow above timeline
                if i + 1 + self.trialOffset == self.curTrial:
                    self.imgIndicator = pygame.image.load(
                        self.imagePath + 'indicator.png')
                    self.indicatorX, self.indicatorY = self.imgIndicator.get_rect().size
                    self.screen.blit(self.imgIndicator, (
                        (self.screen_x / 2) - (self.indicatorX * 6) + (
                            self.indicatorX * i), self.screen_y / 2 - 400))

                # if 2 answers have been selected, draw blue circle for that question
                if data.at[i + self.trialOffset, "user_answer1"] != 0 and \
                                data.at[
                                            i + self.trialOffset, "user_answer2"] != 0:
                    self.imgCircle = pygame.image.load(
                        self.imagePath + 'circleBlue.png')
                else:
                    self.imgCircle = pygame.image.load(
                        self.imagePath + 'circleBlank.png')
                self.circleX, self.circleY = self.imgCircle.get_rect().size
                self.screen.blit(self.imgCircle, (
                    (self.screen_x / 2) - (self.circleX * 6) + (
                        self.circleX * i),
                    self.screen_y / 2 - 350))

            # draw previous button
            self.imgPrev = pygame.image.load(self.imagePath + 'previous.png')
            self.prevX, self.prevY = self.imgPrev.get_rect().size
            self.prevButton = (
                [(self.screen_x / 2) - (self.circleX * 6) - self.prevX - 50,
                 self.screen_y / 2 - 350],
                [(self.screen_x / 2) - (self.circleX * 6) - 50,
                 self.screen_y / 2 - 300])
            self.screen.blit(self.imgPrev,
                             (self.prevButton[0][0], self.prevButton[0][1]))

            # draw next button
            self.imgNext = pygame.image.load(self.imagePath + 'next.png')
            self.nextX, self.nextY = self.imgNext.get_rect().size
            self.nextButton = ([(self.screen_x / 2) + (self.circleX * 6) + 50,
                                self.screen_y / 2 - 350], [
                                   (self.screen_x / 2) + (
                                       self.circleX * 6) + self.nextX + 50,
                                   self.screen_y / 2 - 300])
            self.screen.blit(self.imgNext,
                             (self.nextButton[0][0], self.nextButton[0][1]))

            # draw finish button
            self.imgFinish = pygame.image.load(self.imagePath + 'finish.png')
            self.finishX, self.finishY = self.imgFinish.get_rect().size
            self.finishButton = (
                [(self.screen_x / 2) + (self.circleX * 6) + self.nextX + 60,
                 self.screen_y / 2 - 350], [(self.screen_x / 2) + (
                    self.circleX * 6) + self.nextX + 60 + self.finishX,
                                            self.screen_y / 2 - 300])
            if self.curTrial == 12 or self.curTrial == 24:
                self.screen.blit(self.imgFinish, (
                    self.finishButton[0][0], self.finishButton[0][1]))

            # task boxes
            self.questionX = self.screen_x / 2 - 500  # question box start X position
            self.answerX = self.screen_x / 2 - 200  # answer boxes start X position
            self.spacer = 40  # between answer boxes
            self.letterOffset = 35  # text offset above boxes

            # target image
            imgQ = pygame.image.load(
                self.imagePath + str(self.curTrial) + 'q.png')
            qX, qY = imgQ.get_rect().size
            qButton = ([self.questionX, (self.screen_y / 2) - (qY / 2)],
                       [self.questionX + qX, (self.screen_y / 2) + (qY / 2)])
            self.screen.blit(imgQ, (qButton[0][0], qButton[0][1]))
            lineQ = self.xFont.render("Q" + str(self.curTrial), 1, (0, 0, 0))
            self.screen.blit(lineQ, (
                qButton[0][0], qButton[0][1] - self.letterOffset))

            # answer a
            imgA = pygame.image.load(
                self.imagePath + str(self.curTrial) + 'a.png')
            aX, aY = imgA.get_rect().size
            aButton = ([self.answerX, (self.screen_y / 2) - (aY / 2)],
                       [self.answerX + aX, (self.screen_y / 2) + (aY / 2)])
            self.screen.blit(imgA, (aButton[0][0], aButton[0][1]))
            lineA = self.xFont.render("a", 1, (0, 0, 0))
            self.screen.blit(lineA, (
                aButton[0][0], aButton[0][1] - self.letterOffset))

            # answer b
            imgB = pygame.image.load(
                self.imagePath + str(self.curTrial) + 'b.png')
            bX, bY = imgB.get_rect().size
            bButton = (
                [self.answerX + aX + self.spacer,
                 (self.screen_y / 2) - (bY / 2)],
                [self.answerX + aX + self.spacer + bX,
                 (self.screen_y / 2) + (bY / 2)])
            self.screen.blit(imgB, (bButton[0][0], bButton[0][1]))
            lineB = self.xFont.render("b", 1, (0, 0, 0))
            self.screen.blit(lineB, (
                bButton[0][0], bButton[0][1] - self.letterOffset))

            # answer c
            imgC = pygame.image.load(
                self.imagePath + str(self.curTrial) + 'c.png')
            cX, cY = imgC.get_rect().size
            cButton = ([self.answerX + bX * 2 + self.spacer * 2,
                        (self.screen_y / 2) - (bY / 2)],
                       [self.answerX + bX * 2 + self.spacer * 2 + cX,
                        (self.screen_y / 2) + (bY / 2)])
            self.screen.blit(imgC, (cButton[0][0], cButton[0][1]))
            lineC = self.xFont.render("c", 1, (0, 0, 0))
            self.screen.blit(lineC, (
                cButton[0][0], cButton[0][1] - self.letterOffset))

            # answer d
            imgD = pygame.image.load(
                self.imagePath + str(self.curTrial) + 'd.png')
            dX, dY = imgD.get_rect().size
            dButton = ([self.answerX + cX * 3 + self.spacer * 3,
                        (self.screen_y / 2) - (bY / 2)],
                       [self.answerX + cX * 3 + self.spacer * 3 + dX,
                        (self.screen_y / 2) + (bY / 2)])
            self.screen.blit(imgD, (dButton[0][0], dButton[0][1]))
            lineD = self.xFont.render("d", 1, (0, 0, 0))
            self.screen.blit(lineD, (
                dButton[0][0], dButton[0][1] - self.letterOffset))

            # cache current answers
            self.answer1 = data.at[self.curTrial - 1, 'user_answer1']
            self.answer2 = data.at[self.curTrial - 1, 'user_answer2']

            # check what choices have been made/stored, then draw user choice boxes
            if self.answer1 == 1 or self.answer2 == 1:
                pygame.draw.rect(self.screen, (0, 0, 255), (
                    aButton[0][0], aButton[0][1],
                    aButton[1][0] - aButton[0][0],
                    aButton[1][1] - aButton[0][1]), 5)
            if self.answer1 == 2 or self.answer2 == 2:
                pygame.draw.rect(self.screen, (0, 0, 255), (
                    bButton[0][0], bButton[0][1],
                    bButton[1][0] - bButton[0][0],
                    bButton[1][1] - bButton[0][1]), 5)
            if self.answer1 == 3 or self.answer2 == 3:
                pygame.draw.rect(self.screen, (0, 0, 255), (
                    cButton[0][0], cButton[0][1],
                    cButton[1][0] - cButton[0][0],
                    cButton[1][1] - cButton[0][1]), 5)
            if self.answer1 == 4 or self.answer2 == 4:
                pygame.draw.rect(self.screen, (0, 0, 255), (
                    dButton[0][0], dButton[0][1],
                    dButton[1][0] - dButton[0][0],
                    dButton[1][1] - dButton[0][1]), 5)

            for event in pygame.event.get():
                # check quit
                if event.type == KEYDOWN and event.key == K_F12:
                    main = False
                elif event.type == QUIT:
                    main = False

                # check next previous box clicks
                (mouseX, mouseY) = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.curTrial < self.trialOffset + 12 and mouseX >= \
                        self.nextButton[0][0] and mouseX <= self.nextButton[1][
                    0] and mouseY >= self.nextButton[0][1] and mouseY <= \
                        self.nextButton[1][1]:
                    self.curTrial += 1
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.curTrial > self.trialOffset + 1 and mouseX >= \
                        self.prevButton[0][0] and mouseX <= self.prevButton[1][
                    0] and mouseY >= self.prevButton[0][1] and mouseY <= \
                        self.prevButton[1][1]:
                    self.curTrial -= 1
                if self.curTrial == 12 or self.curTrial == 24:
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouseX >= \
                            self.finishButton[0][0] and mouseX <= \
                            self.finishButton[1][0] and mouseY >= \
                            self.finishButton[0][1] and mouseY <= \
                            self.finishButton[1][1]:
                        main = False

                # check answer box clicks. Upon click, stores value into allData. If empty, then stores value. If value, then clears/set to 0 if clicked again
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouseX >= \
                        aButton[0][0] and mouseX <= aButton[1][0] and mouseY >= \
                        aButton[0][1] and mouseY <= aButton[1][1]:
                    if self.answer1 == 1:
                        data.set_value(self.curTrial - 1, 'user_answer1', 0)
                    elif self.answer2 == 1:
                        data.set_value(self.curTrial - 1, 'user_answer2', 0)
                    else:
                        if self.answer1 == 0:
                            data.set_value(self.curTrial - 1, 'user_answer1',
                                           1)
                        elif self.answer2 == 0:
                            data.set_value(self.curTrial - 1, 'user_answer2',
                                           1)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouseX >= \
                        bButton[0][0] and mouseX <= bButton[1][0] and mouseY >= \
                        bButton[0][1] and mouseY <= bButton[1][1]:
                    if self.answer1 == 2:
                        data.set_value(self.curTrial - 1, 'user_answer1', 0)
                    elif self.answer2 == 2:
                        data.set_value(self.curTrial - 1, 'user_answer2', 0)
                    else:
                        if self.answer1 == 0:
                            data.set_value(self.curTrial - 1, 'user_answer1',
                                           2)
                        elif self.answer2 == 0:
                            data.set_value(self.curTrial - 1, 'user_answer2',
                                           2)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouseX >= \
                        cButton[0][0] and mouseX <= cButton[1][0] and mouseY >= \
                        cButton[0][1] and mouseY <= cButton[1][1]:
                    if self.answer1 == 3:
                        data.set_value(self.curTrial - 1, 'user_answer1', 0)
                    elif self.answer2 == 3:
                        data.set_value(self.curTrial - 1, 'user_answer2', 0)
                    else:
                        if self.answer1 == 0:
                            data.set_value(self.curTrial - 1, 'user_answer1',
                                           3)
                        elif self.answer2 == 0:
                            data.set_value(self.curTrial - 1, 'user_answer2',
                                           3)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouseX >= \
                        dButton[0][0] and mouseX <= dButton[1][0] and mouseY >= \
                        dButton[0][1] and mouseY <= dButton[1][1]:
                    if self.answer1 == 4:
                        data.set_value(self.curTrial - 1, 'user_answer1', 0)
                    elif self.answer2 == 4:
                        data.set_value(self.curTrial - 1, 'user_answer2', 0)
                    else:
                        if self.answer1 == 0:
                            data.set_value(self.curTrial - 1, 'user_answer1',
                                           4)
                        elif self.answer2 == 0:
                            data.set_value(self.curTrial - 1, 'user_answer2',
                                           4)

            pygame.display.flip()

    def run(self):
        # instructions
        # page 1
        instructions = True
        while instructions:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    instructions = False
                elif event.type == KEYDOWN and event.key == K_F12:
                    pygame.quit()
                    exit()

            self.screen.blit(self.background, (0, 0))

            self.title = self.xFont.render("Mental Rotation Task", 1,
                                           (0, 0, 0))
            self.titleW = self.title.get_rect().width
            self.screen.blit(self.title, (
                self.screen_x / 2 - self.titleW / 2, self.screen_y / 2 - 400))

            self.line1 = self.xFont.render(
                "Please look at these five figures:", 1, (0, 0, 0))
            self.screen.blit(self.line1, (100, self.screen_y / 2 - 300))

            img0a = pygame.image.load(self.imagePath + '0a.png')
            x, y = img0a.get_rect().size
            self.screen.blit(img0a, (
                (self.screen_x / 2) - (x / 2), self.screen_y / 2 - 260))

            line2 = self.xFont.render(
                "Note that these are all pictures of the same object which is shown from different angles.",
                1, (0, 0, 0))
            self.screen.blit(line2, (100, self.screen_y / 2 - 60))
            line2a = self.xFont.render(
                "Try to imagine moving the object (or yourself with respect to the object), as you look from one drawing to the next.",
                1, (0, 0, 0))
            self.screen.blit(line2a, (100, self.screen_y / 2 - 10))

            img0b = pygame.image.load(self.imagePath + '0b.png')
            x, y = img0b.get_rect().size
            self.screen.blit(img0b, (
                (self.screen_x / 2) - (x / 2), self.screen_y / 2 + 80))

            line3 = self.xFont.render(
                "Above are two drawings of a new figure that is different from the one shown in the first 5 drawings.",
                1, (0, 0, 0))
            self.screen.blit(line3, (100, self.screen_y / 2 + 280))
            line3a = self.xFont.render(
                "Satisfy yourself that these two drawings show an object that is different, and cannot be rotated to be identical with the object shown in the first five drawings.",
                1, (0, 0, 0))
            self.screen.blit(line3a, (100, self.screen_y / 2 + 330))

            self.pressSpace(100, self.screen_y / 2 + 400)

            pygame.display.flip()

        # page 2 - practice questions
        instructions = True
        practiceCompleted = 0
        while instructions:
            self.screen.blit(self.background, (0, 0))
            line1 = self.xFont.render("Here are 3 practice questions.", 1,
                                      (0, 0, 0))
            self.screen.blit(line1, (100, self.screen_y / 2 - 450))
            line2 = self.xFont.render(
                "For each question, 2 of the 4 pictures show the same object. Click on the 2 matching pictures in each question...",
                1, (0, 0, 0))
            self.screen.blit(line2, (100, self.screen_y / 2 - 400))

            self.questionX = self.screen_x / 2 - 500  # question box start X position
            self.answerX = self.screen_x / 2 - 200  # answer boxes start X position
            self.spacer = 40  # between answer boxes
            self.letterOffset = 35  # text offset above boxes
            # lists used to hold box locations
            qButton = []
            aButton = []
            bButton = []
            cButton = []
            dButton = []
            # draws image boxes, 3 rows. appends location of boxes, for each row, into lists above
            for i in range(3):
                imgQ = pygame.image.load(
                    self.imagePath + "p" + str(i + 1) + 'q.png')
                qX, qY = imgQ.get_rect().size
                qButton.append(([self.questionX,
                                 (self.screen_y / 3) - (qY / 2) + (i * 250)],
                                [self.questionX + qX,
                                 (self.screen_y / 3) + (qY / 2) + (i * 250)]))
                self.screen.blit(imgQ, (qButton[i][0][0], qButton[i][0][1]))
                lineQ = self.xFont.render("Q" + str(i + 1), 1, (0, 0, 0))
                self.screen.blit(lineQ, (
                    qButton[i][0][0], qButton[i][0][1] - self.letterOffset))

                imgA = pygame.image.load(
                    self.imagePath + "p" + str(i + 1) + 'a.png')
                aX, aY = imgA.get_rect().size
                aButton.append(([self.answerX,
                                 (self.screen_y / 3) - (aY / 2) + (i * 250)],
                                [self.answerX + aX,
                                 (self.screen_y / 3) + (aY / 2) + (i * 250)]))
                self.screen.blit(imgA, (aButton[i][0][0], aButton[i][0][1]))
                lineA = self.xFont.render("a", 1, (0, 0, 0))
                self.screen.blit(lineA, (
                    aButton[i][0][0], aButton[i][0][1] - self.letterOffset))

                imgB = pygame.image.load(
                    self.imagePath + "p" + str(i + 1) + 'b.png')
                bX, bY = imgB.get_rect().size
                bButton.append(([self.answerX + aX + self.spacer,
                                 (self.screen_y / 3) - (bY / 2) + (i * 250)],
                                [self.answerX + aX + self.spacer + bX,
                                 (self.screen_y / 3) + (bY / 2) + (i * 250)]))
                self.screen.blit(imgB, (bButton[i][0][0], bButton[i][0][1]))
                lineB = self.xFont.render("b", 1, (0, 0, 0))
                self.screen.blit(lineB, (
                    bButton[i][0][0], bButton[i][0][1] - self.letterOffset))

                imgC = pygame.image.load(
                    self.imagePath + "p" + str(i + 1) + 'c.png')
                cX, cY = imgC.get_rect().size
                cButton.append(([self.answerX + bX * 2 + self.spacer * 2,
                                 (self.screen_y / 3) - (bY / 2) + (i * 250)],
                                [self.answerX + bX * 2 + self.spacer * 2 + cX,
                                 (self.screen_y / 3) + (bY / 2) + (i * 250)]))
                self.screen.blit(imgC, (cButton[i][0][0], cButton[i][0][1]))
                lineC = self.xFont.render("c", 1, (0, 0, 0))
                self.screen.blit(lineC, (
                    cButton[i][0][0], cButton[i][0][1] - self.letterOffset))

                imgD = pygame.image.load(
                    self.imagePath + "p" + str(i + 1) + 'd.png')
                dX, dY = imgD.get_rect().size
                dButton.append(([self.answerX + cX * 3 + self.spacer * 3,
                                 (self.screen_y / 3) - (bY / 2) + (i * 250)],
                                [self.answerX + cX * 3 + self.spacer * 3 + dX,
                                 (self.screen_y / 3) + (bY / 2) + (i * 250)]))
                self.screen.blit(imgD, (dButton[i][0][0], dButton[i][0][1]))
                lineD = self.xFont.render("d", 1, (0, 0, 0))
                self.screen.blit(lineD, (
                    dButton[i][0][0], dButton[i][0][1] - self.letterOffset))

            # draw user choice boxes. checks what value is stored into practiceAnswers[]
            for i in range(3):
                if 1 in self.practiceAnswers[i]:
                    pygame.draw.rect(self.screen, (0, 0, 255), (
                        aButton[i][0][0], aButton[i][0][1],
                        aButton[i][1][0] - aButton[i][0][0],
                        aButton[i][1][1] - aButton[i][0][1]), 5)
                if 2 in self.practiceAnswers[i]:
                    pygame.draw.rect(self.screen, (0, 0, 255), (
                        bButton[i][0][0], bButton[i][0][1],
                        bButton[i][1][0] - bButton[i][0][0],
                        bButton[i][1][1] - bButton[i][0][1]), 5)
                if 3 in self.practiceAnswers[i]:
                    pygame.draw.rect(self.screen, (0, 0, 255), (
                        cButton[i][0][0], cButton[i][0][1],
                        cButton[i][1][0] - cButton[i][0][0],
                        cButton[i][1][1] - cButton[i][0][1]), 5)
                if 4 in self.practiceAnswers[i]:
                    pygame.draw.rect(self.screen, (0, 0, 255), (
                        dButton[i][0][0], dButton[i][0][1],
                        dButton[i][1][0] - dButton[i][0][0],
                        dButton[i][1][1] - dButton[i][0][1]), 5)

            # check answer box clicks
            (mouseX, mouseY) = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    # check all practice questions have been completed before showing answers
                    if 0 not in self.practiceAnswers[0] and 0 not in \
                            self.practiceAnswers[1] and 0 not in \
                            self.practiceAnswers[2]:
                        instructions = False

                # stores values/choices into self.practiceAnswers[]. List value is checked when drawing
                for i in range(3):
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouseX >= \
                            aButton[i][0][0] and mouseX <= aButton[i][1][
                        0] and mouseY >= aButton[i][0][1] and mouseY <= \
                            aButton[i][1][1]:
                        if self.practiceAnswers[i][0] == 1:
                            self.practiceAnswers[i][0] = 0
                        elif self.practiceAnswers[i][1] == 1:
                            self.practiceAnswers[i][1] = 0
                        else:
                            if self.practiceAnswers[i][0] == 0:
                                self.practiceAnswers[i][0] = 1
                            elif self.practiceAnswers[i][1] == 0:
                                self.practiceAnswers[i][1] = 1

                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouseX >= \
                            bButton[i][0][0] and mouseX <= bButton[i][1][
                        0] and mouseY >= bButton[i][0][1] and mouseY <= \
                            bButton[i][1][1]:
                        if self.practiceAnswers[i][0] == 2:
                            self.practiceAnswers[i][0] = 0
                        elif self.practiceAnswers[i][1] == 2:
                            self.practiceAnswers[i][1] = 0
                        else:
                            if self.practiceAnswers[i][0] == 0:
                                self.practiceAnswers[i][0] = 2
                            elif self.practiceAnswers[i][1] == 0:
                                self.practiceAnswers[i][1] = 2

                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouseX >= \
                            cButton[i][0][0] and mouseX <= cButton[i][1][
                        0] and mouseY >= cButton[i][0][1] and mouseY <= \
                            cButton[i][1][1]:
                        if self.practiceAnswers[i][0] == 3:
                            self.practiceAnswers[i][0] = 0
                        elif self.practiceAnswers[i][1] == 3:
                            self.practiceAnswers[i][1] = 0
                        else:
                            if self.practiceAnswers[i][0] == 0:
                                self.practiceAnswers[i][0] = 3
                            elif self.practiceAnswers[i][1] == 0:
                                self.practiceAnswers[i][1] = 3

                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouseX >= \
                            dButton[i][0][0] and mouseX <= dButton[i][1][
                        0] and mouseY >= dButton[i][0][1] and mouseY <= \
                            dButton[i][1][1]:
                        if self.practiceAnswers[i][0] == 4:
                            self.practiceAnswers[i][0] = 0
                        elif self.practiceAnswers[i][1] == 4:
                            self.practiceAnswers[i][1] = 0
                        else:
                            if self.practiceAnswers[i][0] == 0:
                                self.practiceAnswers[i][0] = 4
                            elif self.practiceAnswers[i][1] == 0:
                                self.practiceAnswers[i][1] = 4

            self.pressSpace(100, (self.screen_y / 2) + 450)

            pygame.display.flip()

        # practise answers
        answers = True
        while answers:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    answers = False
            # draws a tick next to the correct answers for practice questions
            imgCorrect = pygame.image.load(self.imagePath + "correct.png")
            correctX, correctY = imgCorrect.get_rect().size
            correctAnswers = [[bButton[0][0], bButton[0][1]],
                              [cButton[0][0], cButton[0][1]],
                              [aButton[1][0], aButton[1][1]],
                              [dButton[1][0], dButton[1][1]],
                              [aButton[2][0], aButton[2][1]],
                              [cButton[2][0], cButton[2][1]]]
            for i in range(6):
                self.screen.blit(imgCorrect,
                                 (correctAnswers[i][0], correctAnswers[i][1]))

            pygame.display.flip()

        # page 3
        instructions = True
        while instructions:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    instructions = False

            self.screen.blit(self.background, (0, 0))
            line1 = self.xFont.render(
                "When you do the test, please remember that for each problem set there are 2, and only 2, figures that match the target figure.",
                1, (0, 0, 0))
            self.screen.blit(line1, (100, self.screen_y / 2 - 200))

            line2 = self.xFont.render(
                "You will only be given a point if you mark off BOTH correct matching figures, marking off only one of these will result in no marks.",
                1, (0, 0, 0))
            self.screen.blit(line2, (100, self.screen_y / 2 - 100))
            line2a = self.xFont.render(
                "Unlike the practice questions, you WON'T be told what the correct answer is.",
                1, (0, 0, 0))
            self.screen.blit(line2a, (100, self.screen_y / 2))

            line3 = self.xFont.render(
                "You will have 3 minutes to complete 12 questions. You may complete them in any order you wish.",
                1, (0, 0, 0))
            self.screen.blit(line3, (100, self.screen_y / 2 + 100))

            self.pressSpace(100, (self.screen_y / 2) + 300)

            pygame.display.flip()

        # page 4
        instructions = True
        while instructions:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    instructions = False

            self.screen.blit(self.background, (0, 0))
            line1 = self.xFont.render("Ready?", 1, (0, 0, 0))
            self.screen.blit(line1, (100, self.screen_y / 2))

            self.pressSpace(100, (self.screen_y / 2) + 100)

            pygame.display.flip()

        # main loop
        self.mainExperiment(1, self.allData)

        # break screen
        breakScreen = True
        while breakScreen:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    breakScreen = False

            self.screen.blit(self.background, (0, 0))
            text = self.xFont.render(
                "Take a quick break. We will do another block of 12 questions when you're ready.",
                1, (0, 0, 0))

            self.screen.blit(text, (100, self.screen_y / 2))

            self.pressSpace(100, (self.screen_y / 2) + 100)

            pygame.display.flip()

        # second half
        self.mainExperiment(2, self.allData)

        # calculate score
        self.accuracy = []
        for i in range(self.allData.shape[0]):
            self.trialCorrect = [self.allData.at[i, 'correct_answer1'],
                                 self.allData.at[i, 'correct_answer2']]
            self.trialUser = [self.allData.at[i, 'user_answer1'],
                              self.allData.at[i, 'user_answer2']]

            if self.trialCorrect[0] in self.trialUser and self.trialCorrect[
                1] in self.trialUser:
                self.accuracy.append(1)
            else:
                self.accuracy.append(0)

        self.allData["correct"] = np.asarray(self.accuracy)

        # rearrange the dataframe
        self.columns = ['trial', 'correct_answer1', 'correct_answer2',
                        'user_answer1', 'user_answer2', 'correct']
        self.allData = self.allData[self.columns]

        # display end screen
        instructions = True
        while instructions:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    instructions = False

            self.screen.blit(self.background, (0, 0))
            endText = self.xFont.render("End of task.", 1, (0, 0, 0))
            self.screen.blit(endText, (100, self.screen_y / 2))

            self.pressSpace(100, (self.screen_y / 2) + 100)

            pygame.display.flip()

        print("- MRT complete")

        return self.allData
