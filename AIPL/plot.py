
import numpy as np

from .shapes import *

EAST, NORTH, WEST, SOUTH = 0, np.pi/2, np.pi, 3/4*np.pi

axis_arrow_size = 10
axis_arrow_angle = 0.4


class DrawableElements:

    offset = np.array([0,0])

    def set_offset(self, offset):
        self.offset = np.array(offset)

    def draw(self, inherited_offset=np.array([0,0])):
        for element in self.elements:
            element.draw(self.offset+inherited_offset)


class Axis(DrawableElements):

    def __init__(self,
        angle: float = 0,
        length: float = 400,
        min_value: float = -1,
        max_value: float = 1,
        origin_value: float = 0,
    ):
        self.angle = angle
        self.length = length
        self.axis_vector = np.array((np.cos(self.angle)*self.length, np.sin(self.angle)*self.length))

        self.min_value = min_value
        self.max_value = max_value
        self.range = self.max_value - self.min_value
        self.origin_value = origin_value
        self.pixels_per_value_unit = self.length / self.range

        self.origin_offset = self.value_to_position(self.origin_value)

        self.vertex0 = -self.origin_offset
        self.vertex1 = -self.origin_offset+self.axis_vector

        self.elements = [
            Lines(
                [self.vertex0, self.vertex1],
                color=(0.2, 0.2, 0.2),
            ),
            self.arrow_lines()
        ]
    
    def value_to_position(self, value):
        return (value - self.min_value) / self.range * self.axis_vector
    
    def position_to_value(self, position):
        return np.linalg.norm(position) / self.length * self.range + self.min_value
    
    def arrow_lines(self):
        return Lines(
            [
                self.vertex1 + axis_arrow_size*np.array((np.cos(self.angle+np.pi-axis_arrow_angle), np.sin(self.angle+np.pi-axis_arrow_angle))),
                self.vertex1,
                self.vertex1 + axis_arrow_size*np.array((np.cos(self.angle+np.pi+axis_arrow_angle), np.sin(self.angle+np.pi+axis_arrow_angle))),
            ],
            color=(0.2, 0.2, 0.2),
            connected=True,
        )


class CartesianPlot(DrawableElements):

    def __init__(self,
        position: tuple[int, int],
        x_axis: Axis,
        y_axis: Axis,
    ):
        self.position = np.array(position)
        super().set_offset(self.position)
        
        self.x_axis = x_axis
        self.y_axis = y_axis

        self.elements = [
            self.x_axis,
            self.y_axis,
            #Lines([self.plot_coord_to_pos((x,y)) for x, y in zip(np.arange(0,10,0.1), map(lambda x: np.sqrt(1-(x/3-2)**2), np.arange(0,10,0.1)))], width=2, connected=True),
            #SquarePoints([self.plot_coord_to_pos((x,y)) for x, y in zip(np.arange(0,10,0.01), map(lambda x: -np.sqrt(1-(x/3-2)**2), np.arange(0,10,0.01)))], size=2),
        ]
    
    def plot_coord_to_pos(self, coord):
        return self.position + self.x_axis.value_to_position(coord[0]) + self.y_axis.value_to_position(coord[1])


class ScatterPlot(DrawableElements):

    def __init__(self, x_values, y_values):
        super().set_offset((100, 100))

        min_x, max_x = min(x_values), max(x_values)
        self.x_margin = (max_x - min_x) * 0.3

        min_y, max_y = min(y_values), max(y_values)
        self.y_margin = (max_y - min_y) * 0.3

        self.cartesian = CartesianPlot(
            (0, 0),
            Axis(EAST, 400, min_x-self.x_margin, max_x+self.x_margin, min_x-self.x_margin),
            Axis(NORTH, 400, min_y-self.y_margin, max_y+self.y_margin, min_y-self.y_margin),
        )

        self.elements = [
            self.cartesian,
            SquarePoints([self.plot_coord_to_pos((x, y)) for x, y in zip(x_values, y_values)], size=6)
        ]

    def plot_coord_to_pos(self, coord):
        return self.cartesian.plot_coord_to_pos(coord) + [self.x_margin, self.y_margin]


# TODO: histograms, heatmaps, trend lines, R^2 values