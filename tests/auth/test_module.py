# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.auth

    for name in pycamunda.auth.__all__:
        getattr(pycamunda.auth, name)
