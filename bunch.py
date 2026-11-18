#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# from warnings import warn
import warnings
import re
import pytest


class BunchMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        newdict = dict(clsdict)
        defaults = {}

        def __init__(self, **kwargs):
            for key, val in defaults.items():
                if key in kwargs:
                    val = kwargs.pop(key)
                setattr(self, key, val)
            if kwargs:
                args = ", ".join(f"{v!r}" for v in kwargs)
                warnings.warn(f"Argument(s) {args} not used")

        def __repr__(self):
            args = ", ".join(
                f"{key}={val2!r}"
                for key, val in defaults.items()
                if (val2 := getattr(self, key)) != val
            )
            return f"{type(self).__name__}({args})"

        newdict = {"__slots__": defaults, "__init__": __init__, "__repr__": __repr__}
        for key, val in clsdict.items():
            if key[:2] == "__" and key[-2:] == "__":
                if key in newdict:
                    raise TypeError(f"Cannot redefine {key}")
            else:
                defaults[key] = val
        return super().__new__(mcls, clsname, bases, newdict)


class Bunch(metaclass=BunchMeta):
    pass


class Exercise(Bunch):
    name: str = "bench press"
    weight: float = 78.5
    reps: int = 2


def test_exercise():
    e = Exercise(name="bench press", weight=78.5, reps=2)
    assert str(e) == "Exercise()"
    e = Exercise(name="squat", weight=60.0, reps=4)
    assert str(e) == "Exercise(name='squat', weight=60.0, reps=4)"
    e = Exercise(reps=10)
    assert str(e) == "Exercise(reps=10)"


def test_redefinition_error():
    with pytest.raises(TypeError, match="Cannot redefine __init__"):

        class E(Bunch):
            def __init__(self):
                pass


def test_bunchmeta_init_userwarning():
    with pytest.raises(UserWarning, match=re.escape("Argument(s) 'set_no' not used")):
        Exercise(name="squat", weight=60.0, reps=4, set_no=3)


if __name__ == "__main__":
    e = Exercise(name="squat", weight=60.0, reps=4)
    print(e)
    e = Exercise(name="squat", weight=60.0, reps=4, set_no=3)
    print(e)
