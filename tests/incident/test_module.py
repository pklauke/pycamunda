# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.incident

    for name in pycamunda.incident.__all__:
        getattr(pycamunda.incident, name)
