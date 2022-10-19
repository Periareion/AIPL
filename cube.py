
from aquaternion import *

side_length = 1
points_per_side = 30
cell_size = side_length / (points_per_side - 1)

cube_vertices = Q((-side_length/2, -side_length/2, -side_length/2))+QuaternionArray([
    *[Q((0+cell_size*(i % points_per_side), 0+cell_size*(i // points_per_side), 0)) for i in range(points_per_side**2)],
    *[Q((0+cell_size*(i % points_per_side), 0, 0+cell_size*(i // points_per_side))) for i in range(points_per_side**2)],
    *[Q((0, 0+cell_size*(i % points_per_side), 0+cell_size*(i // points_per_side))) for i in range(points_per_side**2)],
    *[Q((side_length-cell_size*(i % points_per_side), side_length-cell_size*(i // points_per_side), side_length)) for i in range(points_per_side**2)],
    *[Q((side_length-cell_size*(i % points_per_side), side_length, side_length-cell_size*(i // points_per_side))) for i in range(points_per_side**2)],
    *[Q((side_length, side_length-cell_size*(i % points_per_side), side_length-cell_size*(i // points_per_side))) for i in range(points_per_side**2)],
])

cube_vertices.rotate(qi+2*qj, 1)


from AIPL import *

window = Window(title='AIPL Cube Test', size=(600, 600))

rows = 50
columns = 50

x_min, x_max = -1, 1
x_range = x_max - x_min
y_min, y_max = -1, 1
y_range = y_max - y_min

while True:
    cube_vertices.rotate(qi+qj+qk, 0.1)
    matrix = np.zeros((rows, columns))
    for q in cube_vertices:
        i = int((q.x - x_min) / x_range * columns)
        j = int((q.y - y_min) / y_range * rows)
        matrix[j][i] = max(q.z + 1, matrix[j][i])

    heatmap = plots.HeatMap(
        matrix=matrix,
        gradient=gradients.rainbow,
        size=(400, 400)
    )

    window.render(heatmap, (100, 30))

    window.mainloop_events()