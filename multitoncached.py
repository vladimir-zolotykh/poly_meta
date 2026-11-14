#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from textwrap import dedent
from collections import defaultdict
import pytest


class MultitonCached(type):
    _cached = defaultdict(defaultdict)

    def __call__(cls, *args, **kwargs):
        name = args[0]
        cached = __class__._cached
        if cls not in cached or name not in cached[cls]:
            cached[cls][name] = super().__call__(*args, **kwargs)
        return cached[cls][name]


class Model:

    def __repr__(self):
        args = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{type(self).__name__}({args})"


class Person(Model, metaclass=MultitonCached):
    # _fields = ['name', 'age', 'salary']
    def __init__(self, name, age, salary):
        for k, v in locals().items():
            if k != "self":
                setattr(self, k, v)
        print(f"Initializing {type(self).__name__} {name = }")


class Exercise(Model, metaclass=MultitonCached):
    # _fields = ['name', 'weight', 'reps']
    def __init__(self, name, weight, reps):
        for k, v in locals().items():
            if k != "self":
                setattr(self, k, v)
        print(f"Initializing {type(self).__name__} {name = }")


def test_multitoncached(capsys):
    main()
    assert capsys.readouterr().out == dedent(
        """\
Initializing Person name = 'Bob'
Person(name='Bob', age=37, salary=12000)
Initializing Exercise name = 'squat'
Exercise(name='squat', weight=87, reps=2)
    """
    )


def main():
    bob = Person("Bob", 37, 12000)
    print(bob)
    squat = Exercise("squat", 87, 2)
    print(squat)


if __name__ == "__main__":
    main()
