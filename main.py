#!/usr/bin/env python3

# Nice to have while developing.
import os

from pylaser.output import save
from pylaser.shape import Polyline, Point


pl = Polyline(
    Point(0, 100),
    Point(0, 0),
    Point(100, 0),
)

save('/tmp/pylaser.svg', pl)
save('/tmp/pylaser.dxf', pl)


os.system('firefox /tmp/pylaser.svg')

