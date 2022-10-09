
from AIPL import *

win = Window("Testing", (600, 600))
#plot = CartesianPlot((200,100), Axis(0.2, 300, 0, 10), Axis(2, 200, -2, 2, -2))
plot = ScatterPlot([1,2,3,4,5,6], [1,2,1.5,3,2,3.5])
win.render(plot)
