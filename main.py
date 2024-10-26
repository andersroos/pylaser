#!/usr/bin/env python3

# Nice to have while developing.
import os

from pylaser import Group, Polyline, Point, Circle, BoxEdge, Arc, write

pl = Polyline(
    Point(0, 100),
    Point(0, 0),
    Point(100, 0),
)

ci = Circle(
    Point(100, 100),
    25,
)

be = BoxEdge(Point(100, 100), Point(300, 100), depth=20, length=50, right=False, cut_start=True, cut_end=True)

p = Polyline(Point(50, 75), Point(75, 50))
a1 = Arc(Point(50, 50), 25, 0, 90)
a2 = Arc(Point(50, 50), 30, 10, 135)
a3 = Arc(Point(50, 50), 35, 20, 225)
a4 = Arc(Point(50, 50), 40, 30, 295)

g = Group(
    pl,
    ci,
    be,
    p,
    a1,
    a2,
    a3,
    a4,
    rel=Point(200, 200),
)

write('/tmp/pylaser.svg', g)
write('/tmp/pylaser.dxf', g)


os.system('google-chrome /tmp/pylaser.svg')

