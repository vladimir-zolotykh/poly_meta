#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import BinaryIO
import struct
import copy

polys = [
    [(1.0, 2.5), (3.5, 4.0), (2.5, 1.5)],
    [(7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0)],
    [(3.4, 6.3), (1.2, 0.5), (4.6, 9.2)],
]


def write_polys(f: BinaryIO) -> None:
    num_polys = len(polys)
    f.write(struct.pack("<i", num_polys))
    for _ in range(num_polys):
        for poly in polys:
            f.write(struct.pack("<i", len(poly)))
            for pt in poly:
                f.write(struct.pack("<dd", *pt))


PolysType = list[list[tuple[float, float]]]


def read_polys(f: BinaryIO) -> PolysType:
    num_polys, _ = struct.unpack("<i", f.read(struct.calcsize("<i")))
    polys: PolysType = []
    for _ in range(num_polys):
        num_points, _ = f.read(struct.calcsize("<"))
        poly = []
        for _ in range(num_points):
            poly.appand(struct.unpack("<dd", f.read(struct.calcsize("<dd"))))
        polys.append(poly)
    return polys


def test_write_polys():
    with open("polys.dat", "wb") as f:
        write_polys(f)


def test_read_polys():
    global polys
    expected = copy.deepcopy(polys)
    with open("polys.dat", "rb") as f:
        polys = read_polys(f)
        assert polys == expected
