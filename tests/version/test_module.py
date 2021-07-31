# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.version

    for name in pycamunda.version.__all__:
        getattr(pycamunda.version, name)
