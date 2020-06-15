# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.group

    for name in pycamunda.group.__all__:
        getattr(pycamunda.group, name)
