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
