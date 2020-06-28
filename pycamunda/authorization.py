# -*- coding: utf-8 -*-

"""This module provides access to the authorization REST api of Camunda."""

from __future__ import annotations
import typing
import dataclasses
import enum
import datetime as dt

import requests

import pycamunda
import pycamunda.base
import pycamunda.resource
from pycamunda.request import QueryParameter, PathParameter, BodyParameter

URL_SUFFIX = '/authorization'


__all__ = ['AuthorizationType']


class AuthorizationType(enum.IntEnum):
    global_ = 0
    grant = 1
    revoke = 2


@dataclasses.dataclass
class Authorization:
    """Data class of authorization as returned by the REST api of Camunda."""
    id_: str
    type_: AuthorizationType
    permissions: typing.Tuple[str]
    user_id: str
    group_id: str
    resource_type: pycamunda.resource.ResourceType
    resource_id: str
    links: typing.Tuple[pycamunda.resource.Link]
    root_process_instance_id: str = None
    removal_time: dt.datetime = None

    @classmethod
    def load(cls, data) -> Authorization:
        authorization = cls(
            id_=data['id'],
            type_=data['type'],
            permissions=data['permissions'],
            user_id=data['userId'],
            group_id=data['groupId'],
            resource_type=pycamunda.resource.ResourceType(data['resourceType']),
            resource_id=data['resourceId'],
            links=tuple(pycamunda.resource.Link.load(data=link) for link in data['links'])
        )
        try:
            authorization.removal_time = pycamunda.base.from_isoformat(data['removalTime'])
        except KeyError:
            pass
        try:
            authorization.root_process_instance_id = data['rootProcessInstanceId']
        except KeyError:
            pass

        return authorization
