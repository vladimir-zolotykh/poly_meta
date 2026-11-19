#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


from structmeta import StructMeta, Point, POLYS


class PolyN(metaclass=StructMeta):

    def __init__(self, *pt: Point):
        self._buf = bytearray(self._bufsize)
        for k, p in enumerate(pt):
            setattr(self, self._fields[k], p)


class Poly3(PolyN):
    _fields = ["p0", "p1", "p2"]
    p0 = Point
    p1 = Point
    p2 = Point

    def __repr__(self):
        return f"Poly3({repr(self.p0)}, {repr(self.p1)}, {repr(self.p2)})"


class Poly4(PolyN):
    _fields = ["p0", "p1", "p2", "p3"]
    p0 = Point
    p1 = Point
    p2 = Point
    p3 = Point

    def __repr__(self):
        return (
            f"Poly4({repr(self.p0)}, {repr(self.p1)}, {repr(self.p2)}, {repr(self.p3)})"
        )


class PolyList(PolyN):
    _fields = ["pl0", "pl1", "pl2"]
    pl0 = Poly3
    pl1 = Poly4
    pl2 = Poly3

    def __repr__(self):
        return f"PolyList({repr(self.pl0)}, {repr(self.pl1)}, {repr(self.pl2)})"


if __name__ == "__main__":
    p3 = Poly3(*(Point(*a) for a in POLYS[0]))
    print(p3)
    p4 = Poly4(*(Point(*a) for a in POLYS[1]))
    print(p4)
    p3 = Poly3(*(Point(*a) for a in POLYS[2]))
    print(p3)
    y = PolyList(Poly3(POLYS[0]), Poly4(POLYS[1]), Poly3(POLYS[2]))
    print(y)
