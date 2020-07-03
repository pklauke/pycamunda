# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.authorization

    for name in pycamunda.authorization.__all__:
        getattr(pycamunda.authorization, name)
