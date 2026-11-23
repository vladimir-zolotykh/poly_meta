#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        print(f"{cls = }, {args = }")
        if not Singleton._instance:
            Singleton._instance = super().__call__(*args, **kwargs)
        return Singleton._instance


class Spam(metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        print("Initializing Spam")


def test_spam():
    s1 = Spam(1, 2, 3)
    s2 = Spam()
    assert s1 is s2


if __name__ == "__main__":
    s1 = Spam(1, 2, 3)
    s2 = Spam()
    assert s1 is s2
