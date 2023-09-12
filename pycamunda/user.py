# -*- coding: utf-8 -*-

"""This module provides access to the user REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing

import pycamunda
import pycamunda.resource
import pycamunda.variable
import pycamunda.base
from pycamunda.request import QueryParameter, PathParameter, BodyParameter, BodyParameterContainer

URL_SUFFIX = '/user'


__all__ = [
    'Delete', 'Count', 'GetList', 'GetProfile', 'Options', 'Create', 'UpdateCredentials',
    'UpdateProfile', 'Unlock'
]


@dataclasses.dataclass
class User:
    """Data class of user as returned by the REST api of Camunda."""
    id_: str
    first_name: str
    last_name: str
    email: str = None
    display_name = None

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> User:
        user = cls(
            id_=data['id'],
            first_name=data['firstName'],
            last_name=data['lastName']
        )
        try:
            user.email = data['email']
        except KeyError:
            pass
        try:
            user.display_name = data['displayName']
        except KeyError:
            pass

        return user


class Delete(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str, timeout: int = 5):
        """Deletes a user by id.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request"""
        super().__call__(pycamunda.base.RequestMethod.DELETE, *args, **kwargs, timeout=self.timeout)


class Count(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('id')
    first_name = QueryParameter('firstName')
    first_name_like = QueryParameter('firstNameLike')
    last_name = QueryParameter('lastName')
    last_name_like = QueryParameter('lastNameLike')
    email = QueryParameter('email')
    email_like = QueryParameter('emailLike')
    member_of_group = QueryParameter('memberOfGroup')
    member_of_tenant = QueryParameter('memberOfTenant')

    def __init__(
        self,
        url: str,
        id_: str = None,
        first_name: str = None,
        first_name_like: str = None,
        last_name: str = None,
        last_name_like: str = None,
        email: str = None,
        email_like: str = None,
        member_of_group: str = None,
        member_of_tenant: str = None,
        timeout: int = 5
    ):
        """Count users.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        :param first_name: Filter by the first name of the user.
        :param first_name_like: Filter by a substring of the first name.
        :param last_name: Filter by the last name of the user.
        :param last_name_like: Filter by a substring of the last name.
        :param email: Filter by the email of the user.
        :param email_like: Filter by a substring of the email.
        :param member_of_group: Filter for users which are a member of a group.
        :param member_of_tenant: Filter for users which are a member of a tenant.
        """
        super().__init__(url=url + URL_SUFFIX + '/count')
        self.id_ = id_
        self.first_name = first_name
        self.first_name_like = first_name_like
        self.last_name = last_name
        self.last_name_like = last_name_like
        self.email = email
        self.email_like = email_like
        self.member_of_group = member_of_group
        self.member_of_tenant = member_of_tenant
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> int:
        """Send the request"""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return response.json()['count']


class GetList(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('id')
    first_name = QueryParameter('firstName')
    first_name_like = QueryParameter('firstNameLike')
    last_name = QueryParameter('lastName')
    last_name_like = QueryParameter('lastNameLike')
    email = QueryParameter('email')
    email_like = QueryParameter('emailLike')
    member_of_group = QueryParameter('memberOfGroup')
    member_of_tenant = QueryParameter('memberOfTenant')
    sort_by = QueryParameter(
        'sortBy',
        mapping={
            'id_': 'userId',
            'first_name': 'firstName',
            'last_name': 'lastName',
            'email': 'email'
        }
    )
    ascending = QueryParameter(
        'sortOrder',
        mapping={True: 'asc', False: 'desc'},
        provide=lambda self, obj, obj_type: vars(obj).get('sort_by', None) is not None
    )
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')

    def __init__(
        self,
        url: str,
        id_: str = None,
        first_name: str = None,
        first_name_like: str = None,
        last_name: str = None,
        last_name_like: str = None,
        email: str = None,
        email_like: str = None,
        member_of_group: str = None,
        member_of_tenant: str = None,
        sort_by: str = None,
        ascending: bool = True,
        first_result: int = None,
        max_results: int = None,
        timeout: int = 5
    ):
        """Query for a list of users using a list of parameters. The size of the result set can be
        retrieved by using the Get User Count method.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        :param first_name: Filter by the first name of the user.
        :param first_name_like: Filter by a substring of the first name.
        :param last_name: Filter by the last name of the user.
        :param last_name_like: Filter by a substring of the last name.
        :param email: Filter by the email of the user.
        :param email_like: Filter by a substring of the email.
        :param member_of_group: Filter for users which are a member of a group.
        :param member_of_tenant: Filter for users which are a member of a tenant.
        :param sort_by: Sort the results by `id_`, `first_name`, `last_name` or `email` of the user.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.id_ = id_
        self.first_name = first_name
        self.first_name_like = first_name_like
        self.last_name = last_name
        self.last_name_like = last_name_like
        self.email = email
        self.email_like = email_like
        self.member_of_group = member_of_group
        self.member_of_tenant = member_of_tenant
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> typing.Tuple[User]:
        """Send the request"""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return tuple(User.load(user_json) for user_json in response.json())


class GetProfile(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str, timeout: int = 5):
        """Get the profile of an user.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/profile')
        self.id_ = id_
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> User:
        """Send the request"""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return User.load(response.json())


class Options(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str = None, timeout: int = 5):
        """Get a list of options the currently authenticated user can perform on the user resource.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.id_ = id_
        self.timeout = timeout

    @property
    def url(self):
        return super().url + (f'/{self.id_}' if self.id_ is not None else '')

    def __call__(self, *args, **kwargs) -> pycamunda.resource.ResourceOptions:
        """Send the request"""
        response = super().__call__(pycamunda.base.RequestMethod.OPTIONS, *args, **kwargs, timeout=self.timeout)

        return pycamunda.resource.ResourceOptions.load(response.json())


class Create(pycamunda.base.CamundaRequest):

    id_ = BodyParameter('id')
    first_name = BodyParameter('firstName')
    last_name = BodyParameter('lastName')
    email = BodyParameter('email')
    profile = BodyParameterContainer('profile', id_, first_name, last_name, email)

    password = BodyParameter('password')
    credentials = BodyParameterContainer('credentials', password)

    def __init__(
        self,
        url: str,
        id_: str = None,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        password: str = None,
        timeout: int = 5
    ):
        """Create a new user.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        :param first_name: First name of the user.
        :param last_name: Last name of the user.
        :param email: Email of the user.
        :param password: Password of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/create')
        self.id_ = id_
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request"""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)


class UpdateCredentials(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    password = BodyParameter('password')
    authenticated_user_password = BodyParameter('authenticatedUserPassword')

    def __init__(self, url: str, id_: str, password: str, authenticated_user_password: str, timeout: int = 5):
        """Update a user's credentials (password).

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        :param password: New password of the user.
        :param authenticated_user_password: Password of the authenticated user who changes the
                                            password.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/credentials')
        self.id_ = id_
        self.password = password
        self.authenticated_user_password = authenticated_user_password
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request"""
        super().__call__(pycamunda.base.RequestMethod.PUT, *args, **kwargs, timeout=self.timeout)


class UpdateProfile(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    new_user_id = BodyParameter('id')
    first_name = BodyParameter('firstName')
    last_name = BodyParameter('lastName')
    email = BodyParameter('email')

    def __init__(
        self,
        url: str,
        id_: str,
        new_user_id: str = None,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        timeout: int = 5
    ):
        """Update the profile information of an already existing user.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        :param new_user_id: New user id of the user.
        :param first_name: New first name of the user.
        :param last_name: New last name of the user.
        :param email: New email of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/profile')
        self.id_ = id_
        self.new_user_id = new_user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request"""
        super().__call__(pycamunda.base.RequestMethod.PUT, *args, **kwargs, timeout=self.timeout)


class Unlock(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(
        self,
        url: str,
        id_: str = None,
        timeout: int = 5
    ):
        """Unlock an user.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/unlock')
        self.id_ = id_
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request"""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)
