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


class Person(metaclass=MultitonCached):
    def __init__(self, name, age, salary):
        print(f"Initializing Person {name = }")


class Exercise(metaclass=MultitonCached):
    def __init__(self, name, weight, reps):
        print(f"Initializing Exercise {name = }")


def test_multitoncached(capsys):
    main()


def main():
    bob = Person("Bob", 37, 12000)
    print(bob)
    squat = Exercise("squat", 87, 2)
    print(squat)


if __name__ == "__main__":
    main()
