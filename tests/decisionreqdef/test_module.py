# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.decisionreqdef

    for name in pycamunda.decisionreqdef.__all__:
        getattr(pycamunda.decisionreqdef, name)
