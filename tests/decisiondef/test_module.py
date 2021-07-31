# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.decisiondef

    for name in pycamunda.decisiondef.__all__:
        getattr(pycamunda.decisiondef, name)
