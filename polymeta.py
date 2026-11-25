#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import struct
import textwrap
from write_polys2 import polys, Point


class Field:
    def __init__(self, fmt: str, offset: int = 0):
        self.fmt = fmt
        self.offset = offset

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if isinstance is None:
            return self
        s = slice(self.offset, self.offset + struct.calcsize(self.fmt))
        t = struct.unpack_from(self.fmt, instance._buf[s])
        return self.provide(t)

    def provide(self, t: tuple[float, float]) -> list[tuple[float, float]]:
        return t if len(t) > 1 else t[0]


class FieldWrap(Field):
    def __init__(self, fmt: str, offset: int = 0, wrapper: type = tuple):
        super().__init__(fmt, offset)
        self.wrapper = wrapper

    def provide(
        self, t: tuple[float, float]
    ) -> list[tuple[float, float]] | list[Point]:
        if issubclass(self.wrapper, tuple):
            return [self.wrapper((t[k * 2], t[k * 2 + 1])) for k in range(len(t) // 2)]
        elif issubclass(self.wrapper, Point):
            return [self.wrapper(t[k * 2], t[k * 2 + 1]) for k in range(len(t) // 2)]
        raise TypeError(f"{self.wrapper} must be tuple or Point")


class PolyMeta(type):
    def __new__(mcls, clsname, bases, clsdict, *, model=None, wrapper=tuple):
        offset = 0
        names = []
        offset += struct.calcsize("<i")
        for k, poly in enumerate(model):
            offset += struct.calcsize("<i")
            fmt = "<" + "dd" * len(poly)
            clsdict[name := f"poly{k}"] = FieldWrap(fmt, offset, wrapper)
            names.append(name)
            offset += struct.calcsize(fmt)

        def __iter__(self):
            for a in names:
                yield getattr(self, a)

        clsdict["__iter__"] = __iter__
        clsdict["_bufsize"] = offset
        return super().__new__(mcls, clsname, bases, clsdict)


class PolyP(metaclass=PolyMeta, model=polys, wrapper=Point):
    def __init__(self, buf: bytearray):
        self._buf = bytearray(self._bufsize)
        self._buf = buf


class PolyT(metaclass=PolyMeta, model=polys, wrapper=tuple):
    def __init__(self, buf: bytearray):
        self._buf = bytearray(self._bufsize)
        self._buf = buf


def test_poly_tuple(capsys):
    with open("polys.dat", "rb") as f:
        poly = PolyT(f.read())
        for y in poly:
            print(y)
    assert capsys.readouterr().out == textwrap.dedent(
        """\
[(1.0, 2.5), (3.5, 4.0), (2.5, 1.5)]
[(7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0)]
[(3.4, 6.3), (1.2, 0.5), (4.6, 9.2)]
"""
    )


def test_poly_point(capsys):
    with open("polys.dat", "rb") as f:
        poly = PolyP(f.read())
        for y in poly:
            print(y)
    assert capsys.readouterr().out == textwrap.dedent(
        """\
[Point(1.0, 2.5), Point(3.5, 4.0), Point(2.5, 1.5)]
[Point(7.0, 1.2), Point(5.1, 3.0), Point(0.5, 7.5), Point(0.8, 9.0)]
[Point(3.4, 6.3), Point(1.2, 0.5), Point(4.6, 9.2)]
"""
    )


if __name__ == "__main__":
    test_poly()
