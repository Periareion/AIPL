
import numpy as np

from .constants import *


def create_range(f, start=0, end=1, n=10):
    step = (end - start) / n
    ar = np.arange(start, end, step)
    return ar, list(map(f, ar))


class Function:

    def __init__(self, function, derivative=None, primitive=None):
        self.function = function

        self.derivative = derivative or self.create_derivative()
        self.primitive = primitive or self.create_primitive()

    def __call__(self, *args):
        return self.function(*args)
    
    def create_derivative(self, dx=10e-8):
        self.derivative = lambda x: (self.function(x+dx) - self.function(x)) / dx
        return self.derivative
    
    def create_primitive(self, dx=1e-9):
        return NotImplemented

    def create_range(self, start=0, end=0, n=10):
        return create_range(self, start, end, n)


square = Function(lambda x: x**2, lambda x: 2*x, lambda x: x**3/3)
cube = Function(lambda x: x**3, lambda x: 3*x**2, lambda x: x**4/4)

sqrt = Function(lambda x: x**0.5)
cbrt = Function(lambda x: x**(1/3))

cos = Function(np.cos)
sin = Function(np.sin)