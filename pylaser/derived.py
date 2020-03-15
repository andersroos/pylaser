import math
from pylaser.raw import Point, Box, Polyline


#
# Objects that are combinations of or extensions of basic shapes.
#


class BoxEdge(Polyline):

    def __init__(self, start=None, end=None, depth=None, length=None, right=True,
                 cut_start=False, cut_end=False, min_length=None):
        """ A box edge with cuts from start point to end point.

        :depth: the depth of the cuts
        :length: the length of the cuts
        :right: is the cut (outside) on the right side (True) or the left side (False) in the vector direction
        :cut_start: start with a cut
        :cut_end: end with a cut
        :min_length: when calculating the length at start, this is the min, defaults to depth if None
        """

        if not start or not end or not depth or not length:
            raise Exception("start, end, depth and length are required")

        min_length = depth if min_length is None else min_length

        x_distance = end.x - start.x
        y_distance = end.y - start.y
        distance = math.sqrt(x_distance ** 2 + y_distance ** 2)

        unit_x = x_distance / distance
        unit_y = y_distance / distance

        if right:
            cut_x = -unit_y
            cut_y = unit_x
        else:
            cut_x = unit_y
            cut_y = -unit_x

        # Want to get the cuts in the middle so the first and last step may be shorter. Find out the
        # number of cuts and the start and end distance. Also count needs to be uneven.

        count = int((distance - min_length * 2) // length)
        if cut_end != cut_start:
            # Need even number of cuts.
            count -= count % 2
        else:
            # Need odd number of cuts.
            count -= 1 - count % 2

        end_lengths = (distance - length * count) // 2

        if cut_start:
            start = Point(start.x + cut_x * depth, start.y + cut_y * depth)

        if cut_end:
            end = Point(end.x + cut_x * depth, end.y + cut_y * depth)

        # print("count", count, "end_length", end_length, "distance", distance, "length", length, "min_end_length", min_end_length)

        points = []
        ping = -1 if cut_start else 1

        def add(l, x, y):
            points.append(Point(x, y))
            x += l * unit_x
            y += l * unit_y
            if ping:
                points.append(Point(x, y))
                x += depth * cut_x * ping
                y += depth * cut_y * ping
            return x, y

        x, y = start.x, start.y
        x, y = add(end_lengths, x, y)
        ping = -ping
        for _ in range(count):
            x, y = add(length, x, y)
            ping = -ping
        ping = 0
        add(end_lengths, x, y)
        points.append(end)

        super().__init__(*points)


