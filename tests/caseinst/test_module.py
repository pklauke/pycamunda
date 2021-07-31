# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.caseinst

    for name in pycamunda.caseinst.__all__:
        getattr(pycamunda.caseinst, name)
