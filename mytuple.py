#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter


class TupleMeta(type):
    def __init__(cls, clsname, bases, clsdict):
        # cls: <class 'Tuple'>, <class 'Person'>
        super().__init__(clsname, bases, clsdict)
        fields = clsdict.get("_fields", [])
        for k, name in enumerate(fields):
            setattr(cls, name, property(itemgetter(k)))


class Tuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args, **kwargs):
        # cls: <class 'Person'>
        if (n := len(cls._fields)) != len(args):
            raise TypeError(f"<class {cls.__name__}> gets {n} arguments")
        return super().__new__(cls, args)


class Person(Tuple):
    _fields = ["name", "age", "salary"]


def test_person():
    bob = Person("Bob", 37, 12000)
    assert str(bob) == "('Bob', 37, 12000)"


if __name__ == "__main__":
    test_person()
