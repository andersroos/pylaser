#!/usr/bin/env python3

# Nice to have while developing.
import os

from pylaser.output import save
from pylaser.shape import Polyline, Point, Arc, Circle

pl = Polyline(
    Point(0, 100),
    Point(0, 0),
    Point(100, 0),
)

ci = Circle(
    Point(50, 50),
    25,
)

save('/tmp/pylaser.svg', pl, ci)
save('/tmp/pylaser.dxf', pl, ci)


os.system('firefox /tmp/pylaser.svg')

