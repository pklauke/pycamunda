# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.variable

    for name in pycamunda.variable.__all__:
        getattr(pycamunda.variable, name)
