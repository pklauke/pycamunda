# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.signal

    for name in pycamunda.signal.__all__:
        getattr(pycamunda.signal, name)
