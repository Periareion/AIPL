
import numpy as np

from .geometry import *
from . import utils

EAST, NORTH, WEST, SOUTH = 0, np.pi/2, np.pi, 3/4*np.pi

arrow_tip_size = 10
arrow_tip_angle = 0.4


class PlotPoints2D:

    def __init__(self,
        plot,
        x_values,
        y_values,
        *args,
        **kwargs,
    ):
        self.plot = plot
        self.x_values = x_values
        self.y_values = y_values
        self.args = args
        self.kwargs = kwargs
    
    def draw(self, surface, inherited_offset=np.array((0,0))):
        points = [self.plot.coordinate_to_position((x, y)) for x, y in zip(self.x_values, self.y_values)]
        Lines(*zip(*points), contiguous=True, *self.args, **self.kwargs).draw(surface, inherited_offset)


class CoordinateAxis:

    def __init__(self,
        angle: float = 0,
        length: float = 200,
        min_val: float = -1,
        max_val: float = 1,
        origin: float = -0.5,
        tick_angle: float = None,
    ):
        self.min_val = min_val
        self.max_val = max_val
        self.range = max_val - min_val

        self._setup(angle, length, origin, tick_angle)

        self.tick_angle = tick_angle

        self.generate_drawing_instructions()

    def set_angle(self, angle):
        self._setup(
            angle,
            self.length,
            self.origin,
            self.tick_angle)

    def set_length(self, length):
        self._setup(
            self.angle,
            length,
            self.origin,
            self.tick_angle)

    def set_origin(self, origin):
        self._setup(
            self.angle,
            self.length,
            origin,
            self.tick_angle)
    
    def set_tick_angle(self, tick_angle):
        self._setup(
            self.angle,
            self.length,
            self.origin,
            tick_angle)

    def _setup(self, angle=None, length=None, origin=None, tick_angle=None):
        self.angle = utils.default(EAST, angle)
        self.length = utils.default(200, length)
        self.origin = utils.default(0, origin)
        self.tick_angle = utils.default(self.angle+NORTH, tick_angle)

        self.axis_vector = np.array((np.cos(self.angle)*self.length, np.sin(self.angle)*self.length))
        
        self.origin_offset = self.value_to_position(self.origin)
    
        self.vertex0 = -self.origin_offset
        self.vertex1 = -self.origin_offset+self.axis_vector


    def value_to_position(self, value):
        return (value - self.min_val) / self.range * self.axis_vector

    def position_to_value(self, position):
        return np.linalg.norm(position) / self.length * self.range + self.min_val


    def generate_tick_marks(self, n=10, tick_size=2, tick_angle=np.pi/4):
        tick_positions = [self.vertex0 + k/n*self.axis_vector for k in range(n)]
        return Lines.from_zipped(        
            [tick_positions[k//2] + (-1 if k % 2 else 1)*tick_size*np.array((np.cos(tick_angle), np.sin(tick_angle))) for k in range(2*n)],
            color=(0.2, 0.2, 0.2), width=1,
        )
    
    def generate_arrow_tips(self):
        return Lines.from_zipped(
            [
                self.vertex1 + arrow_tip_size*np.array((np.cos(self.angle+np.pi-arrow_tip_angle), np.sin(self.angle+np.pi-arrow_tip_angle))),
                self.vertex1,
                self.vertex1 + arrow_tip_size*np.array((np.cos(self.angle+np.pi+arrow_tip_angle), np.sin(self.angle+np.pi+arrow_tip_angle))),
            ],
            color=(0.2, 0.2, 0.2),
            contiguous=True,
        )

    def generate_drawing_instructions(self):
        self.drawing_instructions = [
            Lines.from_zipped([self.vertex0, self.vertex1], color=(0.2, 0.2, 0.2), width=1),
            self.generate_tick_marks(tick_angle=utils.default(self.angle+NORTH, self.tick_angle)),
            self.generate_arrow_tips(),
        ]

    def draw(self, surface, inherited_offset=np.array((0,0))):
        for instruction in self.drawing_instructions:
            instruction.draw(surface, inherited_offset)


class Plot:
    
    def __init__(self,
        position: tuple[int, int],
    ):
        self.position = np.array(position)
        
        self.drawing_instructions = []
    
    def draw(self, surface, inherited_offset=np.array((0,0))):
        for instruction in self.drawing_instructions:
            instruction.draw(surface, self.position+inherited_offset)


class Cartesian2D(Plot):

    def __init__(self,
        x_axis: CoordinateAxis = CoordinateAxis(EAST),
        y_axis: CoordinateAxis = CoordinateAxis(NORTH),
        position: tuple[int, int] = (0, 0),
    ):
        super().__init__(position)

        self.x_axis = x_axis
        self.y_axis = y_axis

        self.drawing_instructions.extend([self.x_axis, self.y_axis])
    
    def set_axis_angles(self, x_axis_angle=None, y_axis_angle=None):
        x_axis_angle = utils.default(self.x_axis.angle, x_axis_angle)
        y_axis_angle = utils.default(self.y_axis.angle, y_axis_angle)

        self.x_axis.set_angle(x_axis_angle)
        self.y_axis.set_angle(y_axis_angle)

        self.x_axis.set_tick_angle(y_axis_angle)
        self.y_axis.set_tick_angle(x_axis_angle)

        self.x_axis.generate_drawing_instructions()
        self.y_axis.generate_drawing_instructions()


    def coordinate_to_position(self, coord):
        return self.position + self.x_axis.value_to_position(coord[0]) + self.y_axis.value_to_position(coord[1])


class SingleQuadrantPlot(Cartesian2D):

    def __init__(self,
        x_values,
        y_values,
        size=(400, 400),
        position=(0, 0),
    ):
        self.x_length, self.y_length = size

        self.x_values = x_values
        self.y_values = y_values

        self.max_x, self.min_x = max(self.x_values), min(self.x_values)
        self.max_y, self.min_y = max(self.y_values), min(self.y_values)

        x_axis_angle = EAST
        y_axis_angle = NORTH

        super().__init__(
            CoordinateAxis(x_axis_angle, self.x_length, self.min_x, self.max_x, self.min_x, y_axis_angle),
            CoordinateAxis(y_axis_angle, self.y_length, self.min_y, self.max_y, self.min_y, x_axis_angle),
            position=position,
        )

        #self.points = [self.coordinate_to_position((x, y)) for x, y in zip(self.x_values, self.y_values)]


class ScatterPlot(SingleQuadrantPlot):

    def __init__(self, x_values, y_values, points_type=SquarePoints, **kwargs):
        super().__init__(x_values, y_values, **kwargs)
        self.drawing_instructions.extend([points_type(*zip(*self.points), **kwargs)])


class LinePlot(SingleQuadrantPlot):

    def __init__(self, x_values, y_values, width=3, **kwargs):
        super().__init__(x_values, y_values, **kwargs)
        self.drawing_instructions.extend([PlotPoints2D(self, x_values, y_values)]) #Lines(*zip(*self.points), contiguous=True, width=width)


# TODO: histograms, heatmaps, trend lines, R^2 values