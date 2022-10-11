
import pygame
import numpy as np

from . import graphics

class AbstractPoints:

    def __init__(self, points):
        self.points = points
    
    @classmethod
    def from_axes(cls, x_values, y_values, *args, **kwargs):
        return cls(zip(x_values, y_values), *args, **kwargs)
    
    def unzip(self):
        return zip(self.points)


class Points(AbstractPoints):

    def __init__(self, x_values, y_values, color=(0, 0.5, 1.0)):
        super().__init__(x_values, y_values)
        self.color = color

    def draw(self, surface, offset=np.array((0,0))):
        for point in zip(self.x_values, self.y_values):
            graphics.set_at(surface, offset + point, self.color)


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
        points,
        color = '#2570cd',
        width = 1,
        contiguous: bool = False,
        closed: bool = False,
        smooth: bool = True,
    ):
        self.points = points
        
        self.color = color
        self.width = width

        self.contiguous = contiguous
        self.closed = closed
        self.smooth = smooth

        self.n = len(self.points)

    def draw(self, surface, offset=np.array((0,0))):
        points = [offset + point for point in self.points]

        if self.contiguous:
            graphics.lines(surface, points, self.color, self.smooth, self.width, self.closed)
        else:
            for i in range(0, self.n-1, 2):
                graphics.line(surface, points[i], points[i+1], self.color, self.smooth, self.width)
        