import sdxf
import svgwrite
from svgwrite.container import Group

from pylaser.shape import box


def save(filename, *objs):
    """ Save objects to a file, the format will be selected based on the file ending. Supported formats
    are 'dxf' and 'svg'.
    """

    if filename.endswith('.dxf'):
        _to_dxf(filename, *objs)
    elif filename.endswith('.svg'):
        _to_svg(filename, *objs)
    else:
        raise IOError("Unsupported file ending in filename %s." % filename)


def _to_svg(filename, *objs):

    drawing = svgwrite.Drawing(filename)

    b = box(*(o.box() for o in objs))

    g = Group(transform='translate(0, %d) scale(1, -1)' % int(b.max.y - b.min.y))

    for obj in objs:
        g.add(obj.to_svg())

    drawing.add(g);
    drawing.save()


def _to_dxf(filename, *objs):
    drawing = sdxf.Drawing()

    for obj in objs:
        drawing.append(obj.to_dxf())

    drawing.saveas(filename)

