# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.filter

    for name in pycamunda.filter.__all__:
        getattr(pycamunda.filter, name)
