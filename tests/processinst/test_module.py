# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.processinst

    for name in pycamunda.processinst.__all__:
        getattr(pycamunda.processinst, name)
