
from .colors import *


def gray(t):
    return Color.from_fraction(t*0.5, t*0.8, t)


class ColorHueGradient:
    
    def __init__(self, start=0, end=240, name='Gradient'):
        self.start = start
        self.end = end
        self.name = name
        
        self.hue_gradient_function = self.create_hue_gradient_function()
    
    def create_hue_gradient_function(self):
        return lambda t: Color.from_hsv(t * (self.end - self.start) + self.start, 1, 1)
    
    def __call__(self, t: float):
        return self.hue_gradient_function(t)

rainbow = ColorHueGradient(240, 0, 'Rainbow')
rainbow_inverted = ColorHueGradient(0, 240, 'Inverted rainbow')

blue_to_green = ColorHueGradient(240, 120, 'Blue-Green')
greens_and_blues = ColorHueGradient(120, 240, 'Greens and Blues')
blue_to_cyan = ColorHueGradient(240, 180, 'Blue-Cyan')
cyan_to_magenta = ColorHueGradient(180, 300, 'Cyan-Magenta')
cyan_to_yellow = ColorHueGradient(180, 420, 'Cyan-Yellow')
