from textwrap import dedent
from structmeta import Bbox, Point


def test_bbox(capsys):
    b = Bbox(Point(1, 2), Point(3, 4))
    print(b)
    assert capsys.readouterr().out == dedent(
        """\
Bbox(Point(1.0, 2.0), Point(3.0, 4.0))
    """
    )


def test_bbox_write_read_file():
    b1 = Bbox(Point(10.9, 20.7), Point(70.7, 80.8))
    with open("bbox.dat", "wb") as f:
        f.write(b1._buf)
    b2 = Bbox.__new__(Bbox)
    with open("bbox.dat", "rb") as f:
        b2._buf = f.read(Bbox._bufsize)
    assert b1 == b2
