
import numpy as np

from AIPL import *

def show_gradient(gradient, n=256, width=512, height=200, start=0, end=1):
    value_range = end - start
    step = value_range / n
    m = width // n
    
    window = Window(
        title=f"Gradient: '{gradient}' | {n} samples in the range {start}:{end}",
        size=(width, height),
    )
    
    gradient_values = map(lambda t: gradient(t), np.arange(start, end, step))
    for i, color in enumerate(gradient_values):
        for j in range(m):
            x = m*i + j
            graphics.line(window.surface, (x, 0), (x, height), color)
    
    window.mainloop()

show_gradient(gradients.gray)