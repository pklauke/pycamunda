# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.execution

    for name in pycamunda.execution.__all__:
        getattr(pycamunda.execution, name)
