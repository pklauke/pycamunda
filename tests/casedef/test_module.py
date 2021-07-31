# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.casedef

    for name in pycamunda.casedef.__all__:
        getattr(pycamunda.casedef, name)
