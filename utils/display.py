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

    x_p = mid_x - text_object.get_rect().width/2 if x == "center" else x

    y_p = mix_y - text_object.get_rect().height/2 if y == "center" else y

    screen.blit(text_object, (x_p, y_p))


def space_text(screen, font, x, y, colour=(0, 0, 0)):
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
