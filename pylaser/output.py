import sdxf
import svgwrite


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

    for obj in objs:
        drawing.add(obj.to_svg())

    drawing.save()


def _to_dxf(filename, *objs):
    drawing = sdxf.Drawing()

    for obj in objs:
        drawing.append(obj.to_dxf())

    drawing.saveas(filename)

