# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.tenant

    for name in pycamunda.tenant.__all__:
        getattr(pycamunda.tenant, name)
