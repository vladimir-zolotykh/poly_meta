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


def test_header_write_read():
    h1: Header = Header.default()
    with open("header.dat", "wb") as f:
        f.write(h1._buf)
    h2 = Header.__new__(Header)
    with open("header.dat", "rb") as f:
        h2._buf = f.read(h2._bufsize)
    assert h1 == h2
