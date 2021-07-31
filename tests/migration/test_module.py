# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.migration

    for name in pycamunda.migration.__all__:
        getattr(pycamunda.migration, name)
