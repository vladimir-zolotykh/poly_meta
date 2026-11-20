#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import BinaryIO
import struct
import copy
from structmeta import Point, StructMeta

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


class Sized:
    def __init__(self, buf: bytearray):
        self.buf = buf

    def iter_as(self, what: str | Point) -> tuple | Point:
        sz = struct.calcsize("<dd")
        if isinstance(what, StructMeta):
            assert sz == what._bufsize
        for off in range(len(self.buf) // struct.calcsize("<dd")):
            if isinstance(what, str):
                r: slice = slice(off, off + sz)
                yield struct.unpack_from(what, self.buf[r])
            elif isinstance(what, StructMeta):
                obj = what.__new__(what)
                r: slice = slice(off, what._bufsize)
                obj._buf = self.buf[r]
                yield obj
            else:
                raise TypeError(f"{what!r} must be `str' or `StructMeta'")


def test_sized():
    with open("polys.dat", "rb") as f:
        (num_polys,) = struct.unpack("<i", f.read(struct.calcsize("<i")))
        for _ in range(num_polys):
            num_points = 0
            sized = Sized(f.read(num_points * struct.calcsize("<dd")))
            for t in sized.iter_as("<dd"):
                print(t)


def read_polys(f: BinaryIO) -> PolysType:
    (num_polys,) = struct.unpack("<i", f.read(struct.calcsize("<i")))
    return [
        [
            struct.unpack("<dd", f.read(struct.calcsize("<dd")))
            for _ in range(num_points)
        ]
        for _ in range(num_polys)
        for num_points in struct.unpack("<i", f.read(struct.calcsize("<i")))
    ]


def test_write_polys():
    with open("polys.dat", "wb") as f:
        write_polys(f)


def test_read_polys():
    global polys
    expected = copy.deepcopy(polys)
    with open("polys.dat", "rb") as f:
        polys = read_polys(f)
    assert polys == expected


if __name__ == "__main__":
    with open("polys.dat", "rb") as f:
        res: PolysType = read_polys(f)
    print(res)
