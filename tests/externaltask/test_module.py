# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.externaltask

    for name in pycamunda.externaltask.__all__:
        getattr(pycamunda.externaltask, name)
