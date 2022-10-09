import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Window:


    def __init__(self, title: str, size: tuple[int, int], resizable: bool = True, background_color = (1.0, 1.0, 1.0)):
        width, height = size
        
        self.__title = title
        self.__width = width
        self.__height = height
        self.__resizable = resizable
        self.__background_color = background_color

        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(self.__width, self.__height)
        glutInitWindowPosition(0,0)

        self.__window = glutCreateWindow(self.__title)

    def iterate(self):
        glViewport(0, 0, self.__width, self.__height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.__width, 0.0, self.__height, 0.0, 1.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()

    def render(self, obj=None):

        def show():
            glClearColor(*self.__background_color, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity() # Reset all graphic/shape's position
            self.iterate()
            # draw window here
            obj.draw()

            glutSwapBuffers()

        glutDisplayFunc(show)
        glutIdleFunc(show)
        glutMainLoop()