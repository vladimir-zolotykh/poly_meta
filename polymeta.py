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
        return [tuple((t[k], t[k + 1])) for k in range(len(t) // 2)]


class PolyMeta(type):
    def __new__(mcls, clsname, bases, clsdict, *, model=None):
        offset = 0
        poly_names = []
        npolys = len(model)
        # f.write(struct.pack("<i", num_polys))
        offset += struct.calcsize("<i")
        for _ in range(npolys):
            for k, poly in enumerate(model):
                # f.write(struct.pack("<i", len(poly)))
                offset += struct.calcsize("<i")
                fmt = "<" + "dd" * len(poly)
                poly_names.append(f"poly{k}")
                clsdict[f"poly{k}"] = FieldWrap(fmt, offset)
                offset += struct.calcsize(fmt)

        def __iter__(self):
            for a in poly_names:
                yield getattr(self, a)

        clsdict["__iter__"] = __iter__
        clsdict["_bufsize"] = offset
        return super().__new__(mcls, clsname, bases, clsdict)


class Poly(metaclass=PolyMeta, model=write_polys2.polys):
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
        for a in ("poly0", "poly1", "poly2"):
            yield getattr(self, a)


def test_poly():
    with open("polys.dat", "rb") as f:
        poly = Poly(f.read())
        for y in poly:
            print(y)


if __name__ == "__main__":
    test_poly()
