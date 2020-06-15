# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.activityinst

    for name in pycamunda.activityinst.__all__:
        getattr(pycamunda.activityinst, name)
