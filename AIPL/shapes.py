import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np

class Lines:

    def __init__(self,
        vertices: list[tuple[int, int]],
        color = (0.0, 0.5, 1.0),
        width = 1,
        connected: bool = False,
        closed: bool = False,
    ):

        self.vertices = vertices
        self.color = color
        self.width = width

        self.connected = connected
        self.closed = closed
    
    def draw(self, offset=np.array([0,0])):

        glLineWidth(self.width)
        if self.connected:
            glBegin(GL_LINE_STRIP)
        else:
            glBegin(GL_LINES)

        glColor3fv(self.color)
        n = len(self.vertices)

        for i in range(n):
            glVertex2fv(offset+self.vertices[i])

        if self.closed:
            glVertex2fv(offset+self.vertices[0])

        glEnd()


class Points:

    def __init__(self, points: list[tuple[int, int]]):
        self.points = points
    
    def draw(self, offset=np.array([0,0])):
        glBegin(GL_POINTS)
        for point in self.points:
            glVertex2fv(offset+point)
        glEnd()


class SquarePoints:

    def __init__(self, points: list[tuple[int, int]], color = (0, 0.5, 1.0), size: float = 3):
        self.points = points
        self.color = color
        self.size = size
        self.half_size = size/2
    
    def draw(self, offset=np.array([0,0])):
        glBegin(GL_QUADS)
        glColor3fv(self.color)
        for point in self.points:
            glVertex2fv(offset+point+[-self.half_size, -self.half_size])
            glVertex2fv(offset+point+[+self.half_size, -self.half_size])
            glVertex2fv(offset+point+[+self.half_size, +self.half_size])
            glVertex2fv(offset+point+[-self.half_size, +self.half_size])
        glEnd()


class Polygon:

    def __init__(self,
        vertices: list[tuple[int, int]],
        color=(0.0, 0.5, 1.0),
        *args
    ):
        self.vertices = vertices
        self.color = color
        
    def draw(self, offset=np.array([0,0]), filled=False):
        if filled:
            glBegin(GL_POLYGON)
            glColor3fv(self.color)
            for vertex in self.vertices:
                glVertex2fv(offset+vertex)
            glEnd()
        else:
            Lines(self.vertices, self.color, connected=True, closed=True).draw(offset)


class Rectangle(Polygon):

    def __init__(self, vertices, *args):
        # doesn't check if the vertices actually form a rectangle
        super().__init__(vertices, *args)

    @classmethod
    def from_bottom_left(cls, bottom_left=(0, 0), width=100, height=100, *args):
        bounds = [bottom_left[0], bottom_left[1], bottom_left[0] + width, bottom_left[1] + height]

        vertices = [(bounds[0], bounds[1]),
                    (bounds[2], bounds[1]),
                    (bounds[2], bounds[3]),
                    (bounds[0], bounds[3])]

        return cls(vertices, *args)