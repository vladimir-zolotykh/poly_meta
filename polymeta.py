#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import struct


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
    def provide(self, t: tuple[float, float]) -> list[tuple[float, float]]:
        return [tuple((t[k], t[k + 1])) for k in range(len(t) // 2)]


class PolyMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        offset = 0
        for k, v in clsdict.items():
            if k[:2] == "__" and k[-2:] == "__":
                continue
            if isinstance(v, Field):
                v.offset = offset
                offset += struct.calcsize(v.fmt)
        clsdict["_bufsize"] = offset
        return super().__new__(mcls, clsname, bases, clsdict)


class Poly(metaclass=PolyMeta):
    npolys = Field("<i")
    npoints0 = Field("<i")
    poly0 = FieldWrap("<dddddd")
    npoints1 = Field("<i")
    poly1 = FieldWrap("<dddddddd")
    npoints2 = Field("<i")
    poly2 = FieldWrap("<dddddd")

    def __init__(self, buf: bytearray):
        self._buf = bytearray(self._bufsize)
        self._buf = buf

    def __iter__(self):
        pass


def test_poly():
    with open("polys.dat", "rb") as f:
        poly = Poly(f.read())
        print(poly.npolys)
        print(poly.npoints0)
        print(poly.poly0)
        print(poly.npoints1)
        print(poly.poly1)
        print(poly.npoints2)
        print(poly.poly2)


if __name__ == "__main__":
    test_poly()
