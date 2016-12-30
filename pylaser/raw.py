import math
from collections import namedtuple

import sdxf
import svgwrite

# Basic shapes and objects, output formats should not be known outside this file.


Point = namedtuple('Point', 'x,y')
Box = namedtuple('Box', 'min,max')


STROKE_WIDTH = 1


def box(*objs):
    """ Return a box spanning all objs. """
    boxes = [obj.box() for obj in objs]
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
        return svgwrite.shapes.Polyline(points=[(p.x, p.y) for p in self.points],
                                        fill='none',
                                        stroke='black',
                                        stroke_width=STROKE_WIDTH)

    def to_dxf(self, x_off, y_off):
        return sdxf.PolyLine(points=[(p.x + x_off, p.y + y_off, 0) for p in self.points]),


class Circle(object):

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def box(self):
        return Box(
            Point(self.center.x - self.radius, self.center.y - self.radius),
            Point(self.center.x + self.radius, self.center.y + self.radius),
        )

    def to_dxf(self, x_off, y_off):
        return sdxf.Circle(center=(self.center.x + x_off, self.center.y + y_off), radius=self.radius),

    def to_svg(self):
        return svgwrite.shapes.Circle(center=self.center, r=self.radius,
                                      fill='none',
                                      stroke='black',
                                      stroke_width=STROKE_WIDTH)


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

    def to_svg(self, x_off, y_off):
        # TODO Fix me, dooes not work
        # TODO Use x_off and y off.
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
            stroke_width=2),


class Group(object):

    def __init__(self, *objs, rel=Point(0, 0)):
        """ Make a group and all objects within it is relative to point rel. """
        self.objs = []
        for o in objs:
            self.append(o)
        self.rel = rel

    def append(self, obj):
        if obj:
            self.objs.append(obj)

    def box(self):
        b = box(*self.objs)
        return Box(
            Point(b.min.x + self.rel.x, b.min.y + self.rel.y),
            Point(b.max.x + self.rel.x, b.max.y + self.rel.y),
        )

    def to_svg(self):
        g = svgwrite.container.Group(transform='translate(%d, %d)' % (self.rel.x, self.rel.y))
        for o in self.objs:
            g.add(o.to_svg())
        return g

    def to_dxf(self, x_off, y_off):
        dxfs = []
        for o in self.objs:
            dxfs.extend(o.to_dxf(x_off + self.rel.x, y_off + self.rel.y))
        return dxfs


def write(filename, *objs):
    """ Save objects to a file, the format will be selected based on the file ending. Supported formats
    are 'dxf' and 'svg'.
    """

    if filename.endswith('.dxf'):
        to_dxf(filename, *objs)
    elif filename.endswith('.svg'):
        to_svg(filename, *objs)
    else:
        raise IOError("Unsupported file ending in filename %s." % filename)


def to_svg(filename, *objs):

    drawing = svgwrite.Drawing(filename)

    b = box(*objs)

    g = svgwrite.container.Group(transform='translate(0, %d) scale(1, -1)' % max(b.max.y, b.max.y - b.min.y))

    for obj in objs:
        g.add(obj.to_svg())

    drawing.add(g)
    drawing.save()


def to_dxf(filename, *objs):
    drawing = sdxf.Drawing()

    for obj in objs:
        for dxf in obj.to_dxf(0, 0):
            drawing.append(dxf)

    drawing.saveas(filename)

