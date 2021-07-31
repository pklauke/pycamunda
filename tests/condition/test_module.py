# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.condition

    for name in pycamunda.condition.__all__:
        getattr(pycamunda.condition, name)
