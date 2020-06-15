# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.instruction

    for name in pycamunda.instruction.__all__:
        getattr(pycamunda.instruction, name)
