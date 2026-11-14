#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from textwrap import dedent


class Multiton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        name = args[0]
        insts = __class__._instances
        if name not in insts:
            insts[name] = super().__call__(*args, **kwargs)
        return insts[name]


class Module(metaclass=Multiton):
    def __init__(self, name: str):
        print(f"Initializing {name}")
        self.name = name


class Logger(metaclass=Multiton):
    def __init__(self, name: str):
        print(f"Initializing {name}")
        self.name = name


def test_multiton(capsys):
    main()
    assert capsys.readouterr().out == dedent(
        """\
Initializing tools
Initializing types
Initializing file
Initializing sgream
    """
    )


def main():
    t1 = Module("tools")
    t2 = Module("types")
    t3 = Module("tools")
    assert t1 is not t2
    assert t1 is t3
    g1 = Logger("file")
    g2 = Logger("sgream")
    g3 = Logger("file")
    assert g1 is not g2
    assert g1 is g3


if __name__ == "__main__":
    main()
