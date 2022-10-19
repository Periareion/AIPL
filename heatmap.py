
from AIPL import *

window = Window(title='Heatmap Test',
                size=(600, 600))

matrix = np.zeros((50, 50))

for j in range(50):
    for i in range(50):
        matrix[j][i] = sin((i+4)/6) + cos((j-5)/6)

heatmap = plots.HeatMap(
    matrix=matrix,
    gradient=gradients.cyan_to_magenta,
    size=(400, 400),
)

window.render(heatmap, (100, 100))

window.mainloop()