import sys
import time
import pygame

from pygame.locals import *


def blank_screen(screen, background, duration):
    """Display a blank screen for a certain duration.

    Parameters:
    screen -- pygame screen object used for display
    background -- pygame background that will be displayed
    duration -- duration of the blank screen in milliseconds
    """
    screen.blit(background, (0, 0))
    pygame.display.flip()

    wait(duration)


def text(screen, font, text_string, x, y, colour=(0, 0, 0)):
    """Display onscreen text on screen.

    Parameters:
    screen -- pygame screen object where the text will be displayed
    font -- pygame font object (pygame.font.SysFont(...))
    text_string -- text string to be displayed
    x -- Horizontal position of the text, relative to the window.
        Can be "center" or an integer value
    y -- Vertical position of the text, relative to the window.
        Can be "center" or an integer value
    colour -- tuple containing (Red, Green, Blue) colour values (0-255) of the
        text. Defaults to black (0,0,0)
    """
    text_object = font.render(text_string, 1, colour)

    mid_x = screen.get_width()/2
    mix_y = screen.get_height()/2

    x_p = (mid_x - text_object.get_rect().width/2) if x == "center" else x

    y_p = (mix_y - text_object.get_rect().height/2) if y == "center" else y

    screen.blit(text_object, (x_p, y_p))


def text_space(screen, font, x, y, colour=(0, 0, 0)):
    """Display "press space to continue" text on screen.

    Parameters:
    screen -- pygame screen object where the text will be displayed
    font -- pygame font object (pygame.font.SysFont(...))
    x -- Horizontal position of the text, relative to the window.
        Can be "center" or an integer value
    y -- Vertical position of the text, relative to the window.
        Can be "center" or an integer value
    colour -- tuple containing (Red, Green, Blue) colour values (0-255) of the
        text. Defaults to black (0,0,0)
    """
    text(screen, font, "(press space to continue)", x, y, colour=colour)


def wait(duration):
    """Wait for a certain amount of time before proceeding.

    Parameters:
    duration -- duration of the wait in milliseconds
    """
    start_time = int(round(time.time() * 1000))
    while (int(round(time.time() * 1000)) - start_time) < duration:
        for event in pygame.event.get():
            # TODO add quit hotkey to global Settings
            # Battery will quit if F12 is pressed while waiting
            if event.type == KEYDOWN and event.key == K_F12:
                sys.exit(0)


def wait_for_space():
    """Wait for a spacebar press.

    The current screen will be held until the spacebar, or the `Quit` key,
    is pressed.
    """
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_SPACE:
                waiting = False
            elif event.type == KEYDOWN and event.key == K_F12:
                sys.exit(0)
