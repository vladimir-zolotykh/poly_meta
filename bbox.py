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
        return self.cls._bufsize

    @property
    def rng(self):
        return slice(self.start, self.start + self.size)

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
        offset: int = 0
        for key, val in clsdict.items():
            if key[:2] == "__" and key[-2:] == "__":
                continue
            if isinstance(val, FieldCls):
                val.start = offset
                offset += val.size
        newdict["_bufsize"] = offset
        return super().__new__(mcls, clsname, bases, newdict)


class Bbox(metaclass=StructMeta):
    p1 = FieldCls(Point)
    p2 = FieldCls(Point)

    def __init__(self, p1: Point, p2: Point):
        self._buf = bytearray(self._bufsize)
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f"Bbox({repr(self.p1)}, {repr(self.p2)})"


if __name__ == "__main__":
    b = Bbox(Point(1, 2), Point(3, 4))
    print(b.p1)
    print(b)
