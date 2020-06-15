# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.deployment

    for name in pycamunda.deployment.__all__:
        getattr(pycamunda.deployment, name)
