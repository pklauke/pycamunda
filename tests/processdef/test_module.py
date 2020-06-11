# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.processdef

    for name in pycamunda.processdef.__all__:
        getattr(pycamunda.processdef, name)
