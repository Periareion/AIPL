
from AIPL import *

win = Window("Plot", (600, 500))
plot = LinePlot(*get_points(square, -10, 5, 100), width=3, margin_factor=0.05)
win.render(plot)
