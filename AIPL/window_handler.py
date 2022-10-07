import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class _Window:

    def __init__(self, title, size: tuple[int, int], resizable: bool = True):
        width, height = size
        
        self.__title = title
        self.__width = width
        self.__height = height
        self.__resizable = resizable

    # obj should be a plot object that should be rendered
    def render(self, obj):
        def _clear():
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(self.__width, self.__height)
        glutInitWindowPosition(0,0)

        self.__window = glutCreateWindow(self.__title)
        glutDisplayFunc(_clear)
        glutIdleFunc(_clear)
        glutMainLoop()