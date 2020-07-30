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


__all__ = ['GetGroups', 'VerifyUser', 'GetPasswordPolicy', 'ValidatePassword']


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


@dataclasses.dataclass
class AuthStatus:
    """Data class of the authentication status of an user as returned by the REST api of Camunda."""
    user_id: str
    authenticated: bool

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> AuthStatus:
        return cls(
            user_id=data['authenticatedUser'],
            authenticated=data['authenticated']
        )


@dataclasses.dataclass
class PasswordPolicy:
    """Data class of the password policy as returned by the REST api of Camunda."""
    placeholder: str
    parameters: typing.Dict[str, typing.Any]

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> PasswordPolicy:
        return cls(
            placeholder=data['placeholder'],
            parameters=data['parameters']
        )


@dataclasses.dataclass
class PasswordPolicyCompliance:
    """Data class of the password policy compliance as returned by the REST api of Camunda."""
    policy: PasswordPolicy
    valid: bool

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> PasswordPolicyCompliance:
        policy = PasswordPolicy.load(
            {k: v for k, v in data.items() if k in ('placeholder', 'parameters')}
        )
        return cls(policy=policy, valid=data['valid'])


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


class VerifyUser(pycamunda.base.CamundaRequest):

    username = BodyParameter('username')
    password = BodyParameter('password')

    def __init__(self, url: str, username: str, password: str):
        """Verify the credentials of an user.

        :param url: Camunda Rest engine URL.
        :param username: Name of the user.
        :param password: Password of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/verify')
        self.username = username
        self.password = password

    def __call__(self, *args, **kwargs) -> AuthStatus:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)

        return AuthStatus.load(response.json())


class GetPasswordPolicy(pycamunda.base.CamundaRequest):

    def __init__(self, url: str):
        """Get the list of password policy rules.

        :param url: Camunda Rest engine URL.
        """
        super().__init__(url=url + URL_SUFFIX + '/password-policy')

    def __call__(self, *args, **kwargs) -> typing.Tuple[PasswordPolicy]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return tuple(PasswordPolicy.load(policy_json) for policy_json in response.json()['rules'])


class ValidatePassword(pycamunda.base.CamundaRequest):

    password = BodyParameter('password')

    def __init__(self, url: str, password: str):
        """Validate a password against the password policy rules.

        :param url: Camunda Rest engine URL.
        :param password: Password to validate.
        """
        super().__init__(url=url + URL_SUFFIX + '/password-policy')
        self.password = password

    def __call__(self, *args, **kwargs) -> typing.Tuple[PasswordPolicyCompliance]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)

        return tuple(
            PasswordPolicyCompliance.load(policy_comp_json)
            for policy_comp_json in response.json()['rules']
        )
