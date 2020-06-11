# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.task

    for name in pycamunda.task.__all__:
        getattr(pycamunda.task, name)
