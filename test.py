
from AIPL import *

win = Window("Plot")
plot = LinePlot(*get_points(lambda x: sin(x), 0, 4*tau, 300), size=(300,200))
win.render(plot)
win.mainloop()