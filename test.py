
from AIPL import *

window = Window(size=(600,600))

plot = LinePlot(*get_points(square, start=-1, end=1, n=300), size=(150,150))

for i in range(628):
    plot.set_axis_angles(i/100, i/200+NORTH)
    window.render(plot, (300+30*cos(i/100),300+30*sin(i/100)), True)
    window.mainloop_events()

