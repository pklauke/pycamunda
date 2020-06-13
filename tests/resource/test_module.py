# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.resource

    for name in pycamunda.resource.__all__:
        getattr(pycamunda.resource, name)
