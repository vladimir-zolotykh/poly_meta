#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import BinaryIO, Self
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


class Field:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, owner=None):
        return obj.__dict__[self._name]

    def __set__(self, obj, val):
        obj.__dict__[self._name] = val


class FieldFmt(Field):
    def __init__(self, fmt):
        self.fmt = fmt

    def __set__(self, obj, val):
        super().__set__(obj, val)
        obj._size += struct.calcsize(self.fmt)


class FieldCls(Field):
    def __init__(self, cls):
        self.cls = cls

    def __set__(self, obj, val):
        super().__set__(obj, val)
        obj._size += self.cls._size


class Point:
    x = FieldFmt("<d")
    y = FieldFmt("<d")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def _write(self, f: BinaryIO):
        f.write(struct.pack("<d", self.x))
        f.write(struct.pack("<d", self.y))


class Bbox:
    p1 = FieldCls(Point)
    p2 = FieldCls(Point)

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
    magic = FieldFmt("<i")
    bbox = FieldCls(Bbox)
    num_polys = FieldFmt("<i")

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

    @classmethod
    def default(cls) -> Self:
        bbox = Bbox(POLYS)
        return cls(0x1234, bbox, len(POLYS))

    @classmethod
    def from_file(cls, f: BinaryIO) -> Self:
        buf = f.read(cls._size)
        r1 = slice(0, cls.magic._size)
        r2 = slice(cls.magic._size, cls.bbox._size)
        r3 = slice(cls.bbox._size, cls.num_polys._size)
        return cls(
            struct.unpack("<i", buf[r1])[0],
            Bbox.from_file(buf[r2]),
            struct.unpack("<i", buf[r3])[0],
        )


def write_header(polys: PolysType = POLYS, filename: str = "header.dat") -> None:
    hdr = Header(POLYS)
    with open(filename, "wb") as f:
        hdr._write(f)


def read_header(filename: str = "header.dat") -> Header:
    with open("", "rb") as f:
        hdr: Header = Header.from_file(f)
    return hdr
