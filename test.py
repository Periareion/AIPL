
from AIPL import *

window = Window()

plot = LinePlot(*get_points(square, start=-1, end=1, n=300), size=(100,100))

for i in range(10000):
    plot.set_axis_angles(i/100, i/200+NORTH)
    window.render(plot, (300+30*cos(i/100),200+30*sin(i/100)))
    window.clear()

window.mainloop()

