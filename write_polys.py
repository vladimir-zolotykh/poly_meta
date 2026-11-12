#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
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


class Bbox:
    def __init__(self, polys: PolysType = POLYS):
        self.p1 = Point(
            min(x for x, _ in chain(*polys)), min(y for _, y in chain(*polys))
        )
        self.p2 = Point(
            max(x for x, _ in chain(*polys)), max(y for _, y in chain(*polys))
        )

    def __repr__(self):
        return f"Bbox({self.p1}, {self.p2})"


class Header:
    def __init__(self, polys: PolysType = POLYS):
        self.magic = 0x1234
        self.bbox = Bbox(polys)
        self.num_polys = len(polys)


def write_polys(polys: PolysType = POLYS) -> None:
    pass
