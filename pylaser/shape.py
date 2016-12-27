from collections import namedtuple

import sdxf
import svgwrite.shapes as svg


__doc__ = """
Positive x is right and positive y is up.
"""


Point = namedtuple('Point', 'x,y')


class Polyline(object):

    def __init__(self, *points):
        self.points = points

    def to_svg(self):
        return svg.Polyline(points=[(p.x, -p.y) for p in self.points],
                            fill='none',
                            stroke='black',
                            stroke_width=2)

    def to_dxf(self):
        return sdxf.PolyLine(points=[(p.x, p.y, 0) for p in self.points])
