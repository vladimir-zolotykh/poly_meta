#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Self
import struct
from textwrap import dedent
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
    def __init__(self, name: str, offset: int):
        self._name = name
        self.start = offset

    @property
    def rng(self):
        return slice(self.start, self.start + self.size)


class FieldFmt(Field):
    def __init__(self, name, offset, fmt: str):
        super().__init__(name, offset)
        self.fmt = fmt

    @property
    def size(self):
        return struct.calcsize(self.fmt)

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return struct.unpack(self.fmt, obj._buf[self.rng])[0]

    def __set__(self, obj, val):
        obj._buf[self.rng] = struct.pack(self.fmt, val)


class FieldCls(Field):
    def __init__(self, name, offset, cls: "StructMeta"):
        super().__init__(name, offset)
        self.cls = cls

    @property
    def size(self):
        return self.cls._bufsize

    def __get__(self, instance, owner):
        if instance is None:
            return self
        obj = self.cls.__new__(self.cls)
        obj._buf = instance._buf[self.rng]
        return obj

    def __set__(self, obj, val):
        obj._buf[self.rng] = val._buf


class StructMeta(type):
    def __new__(mcls, clsname, bases, clsdict):

        newdict = dict(clsdict)
        offset = 0
        for key, val in clsdict.items():
            if key[:2] == "__" and key[-2:] == "__":
                continue
            if isinstance(val, (str, StructMeta)):
                typ = FieldFmt if isinstance(val, str) else FieldCls
                fld = typ(key, offset, val)
                newdict[key] = fld
                offset += fld.size
            newdict["_bufsize"] = offset
        return super().__new__(mcls, clsname, bases, newdict)


class Point(metaclass=StructMeta):
    x = "<d"
    y = "<d"

    def __init__(self, x: float, y: float):
        self._buf = bytearray(self._bufsize)
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Bbox(metaclass=StructMeta):
    p1 = Point
    p2 = Point

    def __init__(self, p1: Point, p2: Point):
        self._buf = bytearray(self._bufsize)
        self.p1 = p1
        self.p2 = p2

    @classmethod
    def from_polys(cls, polys: PolysType = POLYS) -> Self:
        p1 = Point(min(x for x, _ in chain(*polys)), min(y for _, y in chain(*polys)))
        p2 = Point(max(x for x, _ in chain(*polys)), max(y for _, y in chain(*polys)))
        return cls(p1, p2)

    def __repr__(self):
        return f"Bbox({repr(self.p1)}, {repr(self.p2)})"


class Header(metaclass=StructMeta):
    magic = "<i"
    bbox = Bbox
    num_polys = "<i"

    def __init__(self, magic: int, bbox: Bbox, num_polys: int):
        self._buf = bytearray(self._bufsize)
        self.magic = magic
        self.bbox = bbox
        self.num_polys = num_polys

    @classmethod
    def default(cls) -> Self:
        bbox = Bbox.from_polys(POLYS)
        return cls(0x1234, bbox, len(POLYS))

    def __repr__(self):
        return f"Header({self.magic}, {repr(self.bbox)}, {self.num_polys})"


def test_point(capsys):
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    print(p1, p2)
    assert capsys.readouterr().out == dedent(
        """\
Point(1.0, 2.0) Point(3.0, 4.0)
    """
    )


def test_bbox(capsys):
    b = Bbox(Point(1, 2), Point(3, 4))
    print(b)
    assert capsys.readouterr().out == dedent(
        """\
Bbox(Point(1.0, 2.0), Point(3.0, 4.0))
    """
    )


def test_header(capsys):
    h: Header = Header.default()
    hdr = Header(h.magic, h.bbox, h.num_polys)
    print(hdr)
    assert capsys.readouterr().out == dedent(
        """\
Header(4660, Bbox(Point(0.5, 0.5), Point(7.0, 9.2)), 3)
"""
    )


if __name__ == "__main__":
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    print(p1, p2)
    print("---------------")
    b = Bbox(Point(1, 2), Point(3, 4))
    print(b)
    print("---------------")
    h: Header = Header.default()
    hdr = Header(h.magic, h.bbox, h.num_polys)
    print(hdr)
