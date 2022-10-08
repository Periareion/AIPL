import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Polygon:

    def __init__(self, vertices: list[tuple[int, int]], color=(0.0, 0.5, 1.0), *args):
        self.vertices = vertices
        self.color = color
        
    def draw(self, filled=False):
        if filled:
            glBegin(GL_POLYGON)
            glColor3f(*self.color)
            for vertex in self.vertices:
                glVertex2f(*vertex)
            glEnd()
        else:
            glBegin(GL_LINES)
            glColor3f(*self.color)
            n = len(self.vertices)
            for i in range(n):
                glVertex2f(*self.vertices[i])
                glVertex2f(*self.vertices[(i+1) % n])
            glEnd()


class Rectangle(Polygon):

    def __init__(self, vertices, *args):
        super().__init__(vertices, *args)

    @classmethod
    def from_bottom_left(cls, bottom_left=(0, 0), width=100, height=100, *args):
        bounds = [bottom_left[0], bottom_left[1], bottom_left[0] + width, bottom_left[1] + height]

        vertices = [(bounds[0], bounds[1]),
                    (bounds[2], bounds[1]),
                    (bounds[2], bounds[3]),
                    (bounds[0], bounds[3])]

        return cls(vertices, *args)