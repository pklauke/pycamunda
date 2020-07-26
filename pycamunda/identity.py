# -*- coding: utf-8 -*-

"""This module provides access to the identity REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing

import pycamunda
import pycamunda.base
import pycamunda.group
import pycamunda.user
from pycamunda.request import QueryParameter, PathParameter, BodyParameter, BodyParameterContainer

URL_SUFFIX = '/identity'


__all__ = [
    'GetGroups'
]


@dataclasses.dataclass
class UsersGroups:
    """Data class of the groups of an user and all of their members as returned by the REST api of
    Camunda."""
    groups: typing.Tuple[pycamunda.group.Group]
    group_users: typing.Tuple[pycamunda.user.User]

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> UsersGroups:
        return cls(
            groups=tuple(pycamunda.group.Group.load(group) for group in data['groups']),
            group_users=tuple(pycamunda.user.User.load(user) for user in data['groupUsers'])
        )


class GetGroups(pycamunda.base.CamundaRequest):

    user_id = QueryParameter('userId')

    def __init__(self, url: str, user_id: str):
        """Get the groups of an user and all of their members.

        :param url: Camunda Rest engine URL.
        :param user_id: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/groups')
        self.user_id = user_id

    def __call__(self, *args, **kwargs) -> UsersGroups:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return UsersGroups.load(response.json())
