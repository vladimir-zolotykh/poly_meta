#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import struct


class FieldFmt:
    def __init__(self, fmt: str):
        self.fmt = fmt

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return struct.unpack(self.fmt, obj.__dict__[self._name])[0]

    def __set__(self, obj, val):
        obj.__dict__[self._name] = struct.pack(self.fmt, val)


class Point:
    x = FieldFmt("<d")
    y = FieldFmt("<d")

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


if __name__ == "__main__":
    p = Point(1, 2)
    print(p.x)
