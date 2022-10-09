
from AIPL import *

window = Window(title='Plot', size=(300,300))

plot = LinePlot(*get_points(square, start=-1, end=1, n=300), size=(200,200))
window.render(plot, (50,50))

window.mainloop()

