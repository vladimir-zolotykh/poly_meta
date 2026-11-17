from textwrap import dedent
from structmeta import Point, Bbox, Header


def test_header(capsys):
    h: Header = Header.default()
    hdr = Header(h.magic, h.bbox, h.num_polys)
    print(hdr)
    assert capsys.readouterr().out == dedent(
        """\
Header(4660, Bbox(Point(0.5, 0.5), Point(7.0, 9.2)), 3)
"""
    )
