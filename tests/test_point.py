from textwrap import dedent
from structmeta import Point


def test_point(capsys):
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    print(p1, p2)
    assert capsys.readouterr().out == dedent(
        """\
Point(1.0, 2.0) Point(3.0, 4.0)
    """
    )


def test_point_write_read_file():
    p1 = Point(1, 2)
    with open("point.dat", "wb") as f:
        f.write(p1._buf)
    p2 = Point.__new__(Point)
    with open("point.dat", "rb") as f:
        p2._buf = f.read(p2._bufsize)
    assert p1 == p2
