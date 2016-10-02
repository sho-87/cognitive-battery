import os
import time
import pandas as pd
import numpy as np
import pygame

from pygame.locals import *
from itertools import product
from sys import exit


class Sternberg(object):
    def __init__(self, screen, blocks=3):
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
        self.background.fill((255, 255, 255))
        pygame.display.set_caption("Sternberg Task")
        pygame.mouse.set_visible(0)

        # create output dataframe
        self.allData = pd.DataFrame()

    def run(self):

        print "- Sternberg Task complete"

        return self.allData
