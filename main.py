#!/usr/bin/env python3

# Nice to have while developing.
import os

from pylaser import Group, Polyline, Point, Circle, BoxEdge, write

pl = Polyline(
    Point(0, 100),
    Point(0, 0),
    Point(100, 0),
)

ci = Circle(
    Point(50, 50),
    25,
)

be = BoxEdge(Point(100, 100), Point(300, 100), depth=20, length=50, right=False, cut_start=True, cut_end=True)

g = Group(pl, ci, be, rel=Point(100, 100))

write('/tmp/pylaser.svg', g)
write('/tmp/pylaser.dxf', g)


os.system('firefox /tmp/pylaser.svg')

