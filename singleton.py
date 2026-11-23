#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import textwrap


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
