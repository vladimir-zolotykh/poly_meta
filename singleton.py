#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import textwrap


class Multiton(type):
    def __init__(cls, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        cls._instances = {}

    def __call__(cls, name, *args, **kwargs):
        if name not in cls._instances:
            cls._instances[name] = super().__call__(name, *args, **kwargs)
        return cls._instances[name]


class Logger(metaclass=Multiton):
    def __init__(self, name: str):
        print(f"Initializing {name!r}")


def test_logger():
    g1 = Logger("g1")
    g2 = Logger("g1")
    assert g1 is g2
    g3 = Logger("g3")
    assert g3 is not g1


class Singleton(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Spam(metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        print("Initializing Spam")


def test_spam():
    s1 = Spam(1, 2, 3)
    s2 = Spam()
    assert s1 is s2


def test_spam_print(capsys):
    test_spam()
    assert capsys.readouterr().out == textwrap.dedent(
        """\
Initializing Spam
"""
    )


if __name__ == "__main__":
    s1 = Spam(1, 2, 3)
    s2 = Spam()
    assert s1 is s2
