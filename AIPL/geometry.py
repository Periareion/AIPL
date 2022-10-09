
import pygame
import numpy as np

from . import graphics

class AbstractPoints:

    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values
    
    @classmethod
    def from_zipped(cls, points, *args, **kwargs):
        return cls(*zip(*points), *args, **kwargs)


class Points(AbstractPoints):

    def __init__(self, x_values, y_values, color=(0, 0.5, 1.0)):
        super().__init__(x_values, y_values)
        self.color = color

    def draw(self, surface, offset=np.array((0,0))):
        for x, y in zip(self.x_values, self.y_values):
            graphics.set_at(surface, offset + (x, y), self.color)


class SquarePoints(AbstractPoints):

    def __init__(self, x_values, y_values,
        color = '#2570cd',
        size: float = 3
    ):
        super().__init__(x_values, y_values)
        self.color = color
        self.size = size
        self.half_size = size/2
    
    def draw(self, surface, offset=np.array((0,0))):
        pass


class Lines(AbstractPoints):

    def __init__(self,
        x_values,
        y_values,
        color = '#2570cd',
        width = 1,
        contiguous: bool = False,
        closed: bool = False,
        smooth: bool = True,
    ):
        self.x_values = x_values
        self.y_values = y_values
        
        self.color = color
        self.width = width

        self.contiguous = contiguous
        self.closed = closed
        self.smooth = smooth

        self.n = len(self.x_values)

    def draw(self, surface, offset=np.array((0,0))):
        points = [offset + (x, y) for x, y in zip(self.x_values, self.y_values)]

        if self.contiguous:
            graphics.lines(surface, points, self.color, self.smooth, self.width, self.closed)
        else:
            for i in range(0, self.n-1, 2):
                graphics.line(surface, points[i], points[i+1], self.color, self.smooth, self.width)
        