#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import struct
import write_polys2


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
        return [tuple((t[k * 2], t[k * 2 + 1])) for k in range(len(t) // 2)]


class PolyMeta(type):
    def __new__(mcls, clsname, bases, clsdict, *, model=None):
        offset = 0
        names = []
        npolys = len(model)
        offset += struct.calcsize("<i")
        for k, poly in enumerate(model):
            offset += struct.calcsize("<i")
            fmt = "<" + "dd" * len(poly)
            names.append(f"poly{k}")
            clsdict[f"poly{k}"] = FieldWrap(fmt, offset)
            offset += struct.calcsize(fmt)

        def __iter__(self):
            for a in names:
                yield getattr(self, a)

        clsdict["__iter__"] = __iter__
        clsdict["_bufsize"] = offset
        return super().__new__(mcls, clsname, bases, clsdict)


class Poly(metaclass=PolyMeta, model=write_polys2.polys):
    def __init__(self, buf: bytearray):
        self._buf = bytearray(self._bufsize)
        self._buf = buf


def test_poly():
    with open("polys.dat", "rb") as f:
        poly = Poly(f.read())
        for y in poly:
            print(y)


if __name__ == "__main__":
    test_poly()
