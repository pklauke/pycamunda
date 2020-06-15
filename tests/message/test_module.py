# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.message

    for name in pycamunda.message.__all__:
        getattr(pycamunda.message, name)
