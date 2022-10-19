
import numpy as np

from .colors import *
from .geometry import *
from . import graphics
from . import utils


EAST, NORTH, WEST, SOUTH = 0, np.pi/2, np.pi, 3/4*np.pi


class Plot:
    
    def __init__(self,
        position: tuple[int, int],
    ):
        self.position = np.array(position)
        
        self.drawing_instructions = []
    
    def draw(self, surface, inherited_offset=np.array((0,0))):
        for instruction in self.drawing_instructions:
            instruction.draw(surface, self.position+inherited_offset)

arrow_tip_size = 10
arrow_tip_angle = 0.4


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
    
        self.axis_tail_pos = -self.origin_offset
        self.axis_head_pos = -self.origin_offset+self.axis_vector


    def value_to_position(self, value):
        return (value - self.min_val) / self.range * self.axis_vector

    def position_to_value(self, position):
        return np.linalg.norm(position) / self.length * self.range + self.min_val


    def generate_tick_marks(self, n=10, tick_size=2, tick_angle=np.pi/4):
        tick_positions = [self.axis_tail_pos + k/n*self.axis_vector for k in range(n)]
        return Lines(        
            [tick_positions[k//2] + (-1 if k % 2 else 1)*tick_size*np.array((np.cos(tick_angle), np.sin(tick_angle))) for k in range(2*n)],
            color=(0.2, 0.2, 0.2), width=1,
        )
    
    def generate_arrow_tips(self):
        return Lines(
            [
                self.axis_head_pos + arrow_tip_size*np.array((np.cos(self.angle+np.pi-arrow_tip_angle), np.sin(self.angle+np.pi-arrow_tip_angle))),
                self.axis_head_pos,
                self.axis_head_pos + arrow_tip_size*np.array((np.cos(self.angle+np.pi+arrow_tip_angle), np.sin(self.angle+np.pi+arrow_tip_angle))),
            ],
            color=(0.2, 0.2, 0.2),
            contiguous=True,
        )

    def generate_drawing_instructions(self):
        self.drawing_instructions = [
            Lines([self.axis_tail_pos, self.axis_head_pos], color=(0.2, 0.2, 0.2), width=2, smooth=False),
            self.generate_tick_marks(tick_angle=utils.default(self.angle+NORTH, self.tick_angle)),
            self.generate_arrow_tips(),
        ]

    def draw(self, surface, inherited_offset=np.array((0,0))):
        for instruction in self.drawing_instructions:
            instruction.draw(surface, inherited_offset)


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


class HeatMap(Cartesian2D):
    
    def __init__(self,
        matrix,
        gradient,
        size=(200, 200),
        position=(0, 0),
        **kwargs
    ):
        matrix -= np.min(matrix)
        matrix /= np.max(matrix)
        self.matrix = matrix
        self.gradient = gradient
        
        self.size = size
        self.x_length, self.y_length = size
        self.position = position

        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0])
        
        self.cell_width = self.size[0] / self.columns
        self.cell_height = self.size[1] / self.rows

        x_axis_angle = EAST
        y_axis_angle = NORTH
        
        super().__init__(
            CoordinateAxis(x_axis_angle, self.x_length, 0, self.columns, 0, y_axis_angle),
            CoordinateAxis(y_axis_angle, self.y_length, 0, self.rows, 0, x_axis_angle),
            position=position,
        )
    
    def draw(self, surface, inherited_offset=np.array((0,0))):
        inherited_offset = np.array(inherited_offset)
        
        x_positions = np.zeros((self.rows+1, self.columns+1))
        y_positions = np.zeros((self.rows+1, self.columns+1))
        
        for j in range(self.rows+1):
            for i in range(self.columns+1):
                x_positions[j][i], y_positions[j][i] = self.coordinate_to_position((i, j))
                #y_positions[j][i] = self.y_length - y_positions[j][i]
        
        
        for j in range(self.rows):
            for i in range(self.columns):
                color = self.gradient(self.matrix[j][i])
                vertices = (
                    inherited_offset + (x_positions[j][i], y_positions[j][i]),
                    inherited_offset + (x_positions[j+1][i], y_positions[j+1][i]),
                    inherited_offset + (x_positions[j+1][i+1], y_positions[j+1][i+1]),
                    inherited_offset + (x_positions[j][i+1], y_positions[j][i+1]),
                )
                graphics.polygon(surface, color, vertices, width=0)
        
        
        for instruction in self.drawing_instructions:
            instruction.draw(surface, self.position+inherited_offset)
        

class SingleQuadrantPlot(Cartesian2D):

    def __init__(self,
        axis_coordinates: tuple[list[float], list[float]]=([0], [0]),
        size=(400, 400),
        position=(0, 0),
        margins=(0.1, 0.1),
    ):
        self.x_length, self.y_length = size

        self.x_values, self.y_values = axis_coordinates

        self.max_x, self.min_x = max(self.x_values), min(self.x_values)
        self.max_y, self.min_y = max(self.y_values), min(self.y_values)
        self.x_margin = (self.max_x - self.min_x) * margins[0]
        self.y_margin = (self.max_y - self.min_y) * margins[1]

        x_axis_angle = EAST
        y_axis_angle = NORTH

        super().__init__(
            CoordinateAxis(x_axis_angle, self.x_length, self.min_x-self.x_margin, self.max_x+self.x_margin, self.min_x-self.x_margin, y_axis_angle),
            CoordinateAxis(y_axis_angle, self.y_length, self.min_y-self.y_margin, self.max_y+self.y_margin, self.min_y-self.y_margin, x_axis_angle),
            position=position,
        )

        #self.points = [self.coordinate_to_position((x, y)) for x, y in zip(self.x_values, self.y_values)]


class PlotCoordinates2D:
    
    def __init__(self,
        plot: Plot,
        coordinates: list[tuple[int, int]],
    ):
        self.plot = plot
        self.coordinates = list(coordinates)
    
    @classmethod
    def from_axes(cls, plot, axis_coordinates):
        return cls(plot, zip(*axis_coordinates))
    
    def draw(self, surface, inherited_offset=np.array((0,0))):
        points = [self.plot.coordinate_to_position(coord) for coord in self.coordinates]
        self.plot.draw_points(points, surface, inherited_offset)


class LinePlot(SingleQuadrantPlot):

    def __init__(self,
        axis_coordinates,
        size=(200, 200),
        position=(0, 0),
        **kwargs
    ):
        super().__init__(axis_coordinates, size=size, position=position)
        self.plot_points = PlotCoordinates2D.from_axes(self, axis_coordinates)
        self.drawing_instructions.extend([self.plot_points])
        self.kwargs = kwargs

    def draw_points(self, points, surface, inherited_offset=np.array((0,0))):
        lines = Lines(points, contiguous=True, **self.kwargs)
        lines.draw(surface, inherited_offset)


class ScatterPlot(SingleQuadrantPlot):

    def __init__(self,
        point_coords,
        points_type=SquarePoints,
        **kwargs
    ):
        super().__init__(point_coords)
        self.kwargs = kwargs
        self.plot_points = PlotCoordinates2D(self, point_coords)
        self.drawing_instructions.extend([self.plot_points])

        self.points_type = points_type
    
    def draw_points(self, points, surface, inherited_offset=np.array((0,0))):
        self.points_type(*zip(*self.points), **self.kwargs).draw(surface, inherited_offset)


# TODO: histograms, heatmaps, trend lines, R^2 values