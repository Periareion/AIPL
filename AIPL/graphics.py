
import pygame


def flip_y(pos, height=500):
    return (pos[0], height-pos[1])

def flip_y_list(position_list, height=500):
    return [flip_y(pos, height) for pos in position_list]


def set_at(surface, position, color):
    surface_height = surface.get_height()
    position = flip_y(position, surface_height)
    surface.set_at(position, color)


def lines(surface, positions, color='#333333', smooth=False, width=1, closed=False):
    surface_height = surface.get_height()
    positions = flip_y_list(positions, surface_height)
    if smooth:
        pygame.draw.aalines(surface, color, closed, positions)
    else:
        pygame.draw.lines(surface, color, closed, positions, width)

def line(surface, start_pos, end_pos, color='#333333', smooth=False, width=1):
    surface_height = surface.get_height()
    start_pos, end_pos = flip_y_list([start_pos, end_pos], surface_height)
    if smooth:
        pygame.draw.aaline(surface, color, start_pos, end_pos)
    else:
        pygame.draw.line(surface, color, start_pos, end_pos, width)