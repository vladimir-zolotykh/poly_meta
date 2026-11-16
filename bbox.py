#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from point import Point


class FieldCls:
    def __init__(self, cls: type):
        self.cls = cls
        self.start = 0

    def __set_name__(self, owner, name):
        self._name = name

    @property
    def size(self):
        return self.cls._size

    @property
    def rng(self):
        return slice(self.start, self.start + self.size)

    def __get__(self, obj, owner):
        if obj is None:
            return self
        clsobj = Point.__new__(self.cls)
        clsobj._buf = obj._buf[self.rng]

    def __set__(self, obj, val):
        obj._buf[self.rng] = val._buf


class StructMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        newdict = dict(clsdict)
        offset = 0
        for key, val in clsdict.items():
            if key[:2] == "__" and key[-2:] == "__":
                continue
            if isinstance(val, FieldCls):
                val.start = offset
                offset += val.size
        newdict["_buf"] = bytearray(offset)
        return super().__new__(mcls, clsname, bases, newdict)


class Bbox(metaclass=StructMeta):
    p1: Point
    p2: Point

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f"Bbox({repr(self.p1)}, {repr(self.p2)})"


if __name__ == "__main__":
    b = Bbox(Point(1, 2), Point(3, 4))
    print(b)
