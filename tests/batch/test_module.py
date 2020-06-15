# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.batch

    for name in pycamunda.batch.__all__:
        getattr(pycamunda.batch, name)
