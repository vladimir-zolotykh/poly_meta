#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import BinaryIO
import struct
from itertools import chain

PointType = tuple[float, float] | list[float]
PolyType = list[PointType]
PolysType = list[PolyType]
POLYS: PolysType = [
    [(1.0, 2.5), (3.5, 4.0), (2.5, 1.5)],
    [(7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0)],
    [(3.4, 6.3), (1.2, 0.5), (4.6, 9.2)],
]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def _write(self, f: BinaryIO):
        f.write(struct.pack("<d", self.x))
        f.write(struct.pack("<d", self.y))


class Bbox:
    def __init__(self, polys: PolysType = POLYS):
        self.p1 = Point(
            min(x for x, _ in chain(*polys)), min(y for _, y in chain(*polys))
        )
        self.p2 = Point(
            max(x for x, _ in chain(*polys)), max(y for _, y in chain(*polys))
        )

    def _write(self, f: BinaryIO):
        self.p1._write(f)
        self.p2._write(f)

    def __repr__(self):
        return f"Bbox({self.p1}, {self.p2})"


class Header:
    def __init__(self, polys: PolysType = POLYS):
        self.magic = 0x1234
        self.bbox = Bbox(polys)
        self.num_polys = len(polys)

    def __repr__(self):
        return f"Header({self.magic}, {repr(self.bbox)}, {self.num_polys})"

    def _write(self, f: BinaryIO) -> None:
        f.write(struct.pack("<i", self.magic))
        self.bbox._write(f)
        f.write(struct.pack("<i", self.num_polys))


def write_polys(polys: PolysType = POLYS, filename: str = "header.dat") -> None:
    hdr = Header(POLYS)
    with open(filename, "wb") as f:
        hdr._write(f)
