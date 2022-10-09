
import numpy as np

from .geometry import *

EAST, NORTH, WEST, SOUTH = 0, np.pi/2, np.pi, 3/4*np.pi

axis_arrow_size = 10
axis_arrow_angle = 0.4


class CoordinateAxis:

    def __init__(self,
        angle: float = 0,
        length: float = 400,
        min_value: float = -1,
        max_value: float = 1,
        origin_value: float = 0,
        margin_factor: float = 0.1,
        tick_angle: float = None,
    ):
        self.angle = angle
        self.length = length
        self.axis_vector = np.array((np.cos(self.angle)*self.length, np.sin(self.angle)*self.length))

        self.margin = (max_value - min_value) * margin_factor

        self.min_value = min_value - self.margin
        self.max_value = max_value + self.margin
        self.range = self.max_value - self.min_value
        self.origin_value = origin_value - self.margin
        self.pixels_per_value_unit = self.length / self.range

        self.origin_offset = self.value_to_position(self.origin_value)

        self.vertex0 = -self.origin_offset
        self.vertex1 = -self.origin_offset+self.axis_vector

        self.tick_angle = tick_angle

        self.elements = [
            Lines.from_zipped(
                [self.vertex0, self.vertex1],
                color=(0.2, 0.2, 0.2),
                width=1,
            ),
            self.generate_tick_marks(tick_angle=(self.angle+NORTH if self.tick_angle is None else self.tick_angle)),
            self.generate_arrow_lines(),
        ]

    def value_to_position(self, value):
        return (value - self.min_value) / self.range * self.axis_vector

    def position_to_value(self, position):
        return np.linalg.norm(position) / self.length * self.range + self.min_value

    def generate_tick_marks(self, n=10, tick_size=2, tick_angle=np.pi/4):
        tick_positions = [self.vertex0 + k/n*self.axis_vector for k in range(n)]
        return Lines.from_zipped(        
            [tick_positions[k//2] + (-1 if k % 2 else 1)*tick_size*np.array((np.cos(tick_angle), np.sin(tick_angle))) for k in range(2*n)],
            color=(0.2, 0.2, 0.2), width=1,
        )
    
    def generate_arrow_lines(self):
        return Lines.from_zipped(
            [
                self.vertex1 + axis_arrow_size*np.array((np.cos(self.angle+np.pi-axis_arrow_angle), np.sin(self.angle+np.pi-axis_arrow_angle))),
                self.vertex1,
                self.vertex1 + axis_arrow_size*np.array((np.cos(self.angle+np.pi+axis_arrow_angle), np.sin(self.angle+np.pi+axis_arrow_angle))),
            ],
            color=(0.2, 0.2, 0.2),
            contiguous=True,
        )

    def draw(self, surface, inherited_offset=np.array([0,0])):
        for element in self.elements:
            element.draw(surface, inherited_offset)


class Cartesian2D:

    def __init__(self,
        position: tuple[int, int],
        x_axis: CoordinateAxis,
        y_axis: CoordinateAxis,
    ):
        self.position = np.array(position)
        self.x_axis = x_axis
        self.y_axis = y_axis

        self.elements = [
            self.x_axis,
            self.y_axis,
        ]
    
    def coord_to_pos(self, coord):
        return self.position + self.x_axis.value_to_position(coord[0]) + self.y_axis.value_to_position(coord[1])

    def draw(self, surface, inherited_offset=np.array([0,0])):
        for element in self.elements:
            element.draw(surface, self.position+inherited_offset)


class SingleQuadrantPlot:

    def __init__(self,
        x_values,
        y_values,
        margin_factor=0.1,
        size=(400, 400)
    ):
        self.position = np.array([100, 100])

        self.x_values = x_values
        self.y_values = y_values
        
        self.margin_factor = margin_factor
        self.x_axis_length, self.y_axis_length = self.size = size

        self.max_x, self.min_x = max(self.x_values), min(self.x_values)

        self.max_y, self.min_y = max(self.y_values), min(self.y_values)

        x_axis_angle = EAST
        y_axis_angle = NORTH

        self.coordinate_system = Cartesian2D(
            (0, 0),
            CoordinateAxis(
                x_axis_angle, self.x_axis_length, 
                self.min_x, self.max_x, self.min_x,
                margin_factor=self.margin_factor, tick_angle=y_axis_angle
            ),
            CoordinateAxis(
                y_axis_angle, self.y_axis_length,
                self.min_y, self.max_y, self.min_y,
                margin_factor=self.margin_factor, tick_angle=x_axis_angle
            ),
        )

        self.points = [self.coord_to_pos((x, y)) for x, y in zip(self.x_values, self.y_values)]

        self.elements = [
            self.coordinate_system,
        ]

    def coord_to_pos(self, coord):
        return self.coordinate_system.coord_to_pos(coord)

    def draw(self, surface, inherited_offset=np.array([0,0])):
        for element in self.elements:
            element.draw(surface, self.position+inherited_offset)


class ScatterPlot(SingleQuadrantPlot):

    def __init__(self, x_values, y_values, points_type=SquarePoints, **kwargs):
        super().__init__(x_values, y_values, **kwargs)
        self.elements.extend([points_type(*zip(*self.points), **kwargs)])


class LinePlot(SingleQuadrantPlot):

    def __init__(self, x_values, y_values, width=3, **kwargs):
        super().__init__(x_values, y_values, **kwargs)
        self.elements.extend([Lines(*zip(*self.points), contiguous=True, width=width)])


# TODO: histograms, heatmaps, trend lines, R^2 values