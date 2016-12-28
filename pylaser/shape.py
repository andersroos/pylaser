import math
from collections import namedtuple

import sdxf
import svgwrite

__doc__ = """
Positive x is right and positive y is up.
"""


Point = namedtuple('Point', 'x,y')


Box = namedtuple('Box', 'min,max')


#
# translation = move = add
# scale = flip
#


def box(*boxes):
    """ Return a box spanning all boxes. """
    return Box(
        Point(min(b.min.x for b in boxes), min(b.min.y for b in boxes)),
        Point(max(b.max.x for b in boxes), max(b.max.y for b in boxes)),
    )


class Polyline(object):

    def __init__(self, *points):
        self.points = points

    def box(self):
        return Box(
            Point(min(p.x for p in self.points), min(p.y for p in self.points)),
            Point(max(p.x for p in self.points), max(p.y for p in self.points)),
        )

    def to_svg(self):
        # TODO Svg y is down, fix this with some transform.
        return svgwrite.shapes.Polyline(points=[(p.x, p.y) for p in self.points],
                                        fill='none',
                                        stroke='black',
                                        stroke_width=2)

    def to_dxf(self):
        return sdxf.PolyLine(points=[(p.x, p.y, 0) for p in self.points])


class Circle(object):

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def box(self):
        return Box(
            Point(self.center.x - self.radius, self.center.y - self.radius),
            Point(self.center.x + self.radius, self.center.y + self.radius),
        )

    def to_dxf(self):
        return sdxf.Circle(center=(self.center.x,self.center.y), radius=self.radius)

    def to_svg(self):
        return svgwrite.shapes.Circle(center=self.center, r=self.radius,
                                      fill='none',
                                      stroke='black',
                                      stroke_width=2)


class Arc(object):

    def __init__(self, center, radius, start_angle=0, end_angle=360):
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle

    def box(self):
        # TODO Fix this when using angles.
        return Box(
            Point(self.center.x - self.radius, self.center.y - self.radius),
            Point(self.center.x + self.radius, self.center.y + self.radius),
        )

    def to_dxf(self):
        return sdxf.Arc(center=(self.center.x,self.center.y),
                        radius=self.radius,
                        startAngle=self.start_angle,
                        endAngle=self.end_angle)

    def to_svg(self):
        # TODO Fix me, dooes not work
        return svgwrite.path.Path(d=[
            'M',
            (self.center.x + self.radius * math.cos(self.start_angle * 2 * math.pi / 360),
             self.center.y + self.radius * math.sin(self.start_angle * 2 * math.pi / 360)),
            'A',
            (self.center.x, self.center.y),
            0,
            0,  # small/large
            0,  # clockwise/anti
            (self.center.x + self.radius * math.cos(self.end_angle * 2 * math.pi / 360),
             self.center.y + self.radius * math.sin(self.end_angle * 2 * math.pi / 360)),
        ],
            fill='none',
            stroke='black',
            stroke_width=2)
