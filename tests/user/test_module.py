# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.user

    for name in pycamunda.user.__all__:
        getattr(pycamunda.user, name)
