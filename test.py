
from AIPL import *

window = Window(size=(600,600))

plot = plots.LinePlot(create_range(sin, start=-pi, end=pi, n=100), size=(200,200))
window.render(plot, (300,300))
window.mainloop()

#for i in range(6280):
#    plot.set_axis_angles(i/100, i/200+NORTH)
#    window.render(plot, (300+30*cos(i/100),300+30*sin(i/100)), True)
#    window.mainloop_events(True)
