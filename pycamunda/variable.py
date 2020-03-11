# -*- coding: utf-8 -*-

"""This module provides utilities for the variable formats Camunda uses."""

import datetime as dt
import dataclasses
import typing


@dataclasses.dataclass
class Variable:
    value: typing.Any
    type: str
    value_info: typing.Dict


def isoformat(datetime_):
    """Convert a datetime object to the isoformat string Camunda expects. Datetime objects are
    expected to contain timezoneinformation.

    :param datetime_: Datetime object to convert.
    :return: Isoformat datetime string.
    """
    if isinstance(datetime_, dt.datetime):
        dt_str = datetime_.strftime('%Y-%m-%dT%H:%M:%S.{ms}%z')
        ms = datetime_.microsecond // 1000
        dt_str = dt_str.format(ms=str(ms).zfill(3))
    else:
        dt_str = datetime_.strftime('%Y-%m-%d')

    return dt_str
