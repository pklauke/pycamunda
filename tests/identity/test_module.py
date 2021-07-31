# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.identity

    for name in pycamunda.identity.__all__:
        getattr(pycamunda.identity, name)
