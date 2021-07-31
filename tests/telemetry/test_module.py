# -*- coding: utf-8 -*-


def test_all_contains_only_valid_names():
    import pycamunda.telemetry

    for name in pycamunda.telemetry.__all__:
        getattr(pycamunda.telemetry, name)
