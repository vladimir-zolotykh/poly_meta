#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from warnings import warn


class Bunch(type):
    def __new__(mcls, clsname, bases, clsdict):
        newdict = dict(clsdict)
        defaults = {}

        def __init__(self, **kwargs):
            for key, val in defaults.items():
                if key in kwargs:
                    val = kwargs.pop(key)
                setattr(self, key, val)
            if kwargs:
                raise warn(f"No variables left for {kwargs.keys()!r}")

        def __repr__(self):
            args = ", ".join(
                f"{key}={val!r}"
                for key, val in defaults.items()
                if getattr(self, key) != val
            )
            return f"{type(self).__name__}({args})"

        newdict = {"__slots__": defaults, "__init__": __init__, "__repr__": __repr__}
        for key, val in clsdict.items():
            if key[:2] == "__" and key[-2:] == "__":
                if key in newdict:
                    raise TypeError(f"Cannot redefine {key}")
            else:
                defaults.append(key)
                # newdict.__slots__.append(key)
        return super().__new__(mcls, clsname, bases, newdict)


class Exercise(Bunch):
    name: str = "bench press"
    weight: float = 78.5
    reps: int = 2


if __name__ == "__main__":
    e = Exercise()
    print(e)
