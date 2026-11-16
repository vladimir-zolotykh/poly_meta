#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Self
import struct


class FieldFmt:
    def __init__(self, fmt: str):
        self.fmt = fmt
        self.start = 0

    def __set_name__(self, owner, name):
        self._name = name

    @property
    def size(self):
        return struct.calcsize(self.fmt)

    @property
    def rng(self):
        return slice(self.start, self.start + self.size)

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return struct.unpack(self.fmt, obj._buf[self.rng])[0]

    def __set__(self, obj, val):
        obj._buf[self.rng] = struct.pack(self.fmt, val)


class StructMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        newdict = dict(clsdict)
        offset = 0
        for key, val in clsdict.items():
            if key[:2] == "__" and key[-2:] == "__":
                continue
            if isinstance(val, FieldFmt):
                val.start = offset
                offset += val.size
        newdict["_buf"] = bytearray(offset)
        return super().__new__(mcls, clsname, bases, newdict)


class Point(metaclass=StructMeta):
    x = FieldFmt("<d")
    y = FieldFmt("<d")

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


if __name__ == "__main__":
    p = Point(1, 2)
    print(p.x, p.y)
