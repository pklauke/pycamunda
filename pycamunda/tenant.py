# -*- coding: utf-8 -*-

"""This module provides access to the tenant REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing

import pycamunda
import pycamunda.base
import pycamunda.resource
from pycamunda.request import QueryParameter, PathParameter, BodyParameter

URL_SUFFIX = '/tenant'
URL_SUFFIX_USER_MEMBERS = '/user-members'
URL_SUFFIX_GROUP_MEMBERS = '/group-members'


__all__ = [
    'UserMemberCreate', 'UserMemberDelete', 'UserMemberOptions', 'GroupMemberCreate',
    'GroupMemberDelete', 'GroupMemberOptions', 'GetList', 'Count', 'Get', 'Create', 'Update',
    'Options', 'Delete'
]


@dataclasses.dataclass
class Tenant:
    """Data class of tenant as returned by the REST api of Camunda."""
    id_: str
    name: str

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> Tenant:
        return cls(id_=data['id'], name=data['name'])


class UserMemberCreate(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    user_id = PathParameter('userId')

    def __init__(self, url: str, id_: str, user_id: str):
        """Create a membership between a tenant and an user.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the tenant.
        :param user_id: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}' + URL_SUFFIX_USER_MEMBERS + '/{userId}')
        self.id_ = id_
        self.user_id = user_id

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.PUT, *args, **kwargs)


class UserMemberDelete(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    user_id = PathParameter('userId')

    def __init__(self, url: str, id_: str, user_id: str):
        """Delete a membership between a tenant and an user.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the tenant.
        :param user_id: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}' + URL_SUFFIX_USER_MEMBERS + '/{userId}')
        self.id_ = id_
        self.user_id = user_id

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.DELETE, *args, **kwargs)


class UserMemberOptions(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get a list of options the currently authenticated user can perform on the tenant
        membership resource.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the tenant.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}' + URL_SUFFIX_USER_MEMBERS)
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> pycamunda.resource.ResourceOptions:
        """Send the request"""
        response = super().__call__(pycamunda.base.RequestMethod.OPTIONS, *args, **kwargs)

        return pycamunda.resource.ResourceOptions.load(response.json())


class GroupMemberCreate(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    group_id = PathParameter('groupId')

    def __init__(self, url: str, id_: str, group_id: str):
        """Create a membership between a tenant and a group.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the tenant.
        :param group_id: Id of the group.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}' + URL_SUFFIX_GROUP_MEMBERS + '/{groupId}')
        self.id_ = id_
        self.group_id = group_id

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.PUT, *args, **kwargs)


class GroupMemberDelete(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    group_id = PathParameter('groupId')

    def __init__(self, url: str, id_: str, group_id: str):
        """Delete a membership between a tenant and a group.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the tenant.
        :param group_id: Id of the group.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}' + URL_SUFFIX_GROUP_MEMBERS + '/{groupId}')
        self.id_ = id_
        self.group_id = group_id

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.DELETE, *args, **kwargs)


class GroupMemberOptions(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get a list of options the currently authenticated user can perform on the tenant
        membership resource.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the tenant.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}' + URL_SUFFIX_GROUP_MEMBERS)
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> pycamunda.resource.ResourceOptions:
        """Send the request"""
        response = super().__call__(pycamunda.base.RequestMethod.OPTIONS, *args, **kwargs)

        return pycamunda.resource.ResourceOptions.load(response.json())


class GetList(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('id')
    name = QueryParameter('name')
    name_like = QueryParameter('nameLike')
    user_member = QueryParameter('userMember')
    group_member = QueryParameter('groupMember')
    including_groups_of_user = QueryParameter(
        'includingGroupsOfUser',
        provide=pycamunda.base.value_is_true
    )
    sort_by = QueryParameter('sortBy', mapping={'id_': 'id', 'name': 'name'})
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
        name: str = None,
        name_like: str = None,
        user_member: str = None,
        group_member: str = None,
        including_groups_of_user: bool = False,
        sort_by: str = None,
        ascending: bool = True,
        first_result: int = None,
        max_results: int = None
    ):
        """Query for a list of tenants using a list of parameters. The size of the result set can be
        retrieved by using the Count class.

        :param url: Camunda Rest engine URL.
        :param id_: Filter by the id of the tenant.
        :param name: Filter by the name of the tenant.
        :param name_like: Filter by a substring of the name.
        :param user_member: Filter for tenants where the given user is member of.
        :param group_member: Filter for tenants where  the given group is a member of.
        :param including_groups_of_user: Filter for tenants where the user or one of his groups is a
                                         member of. Can only be used with `user_member` parameter.
        :param sort_by: Sort the results by `id_` or `name` of the tenant.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.id_ = id_
        self.name = name
        self.name_like = name_like
        self.user_member = user_member
        self.group_member = group_member
        self.including_groups_of_user = including_groups_of_user
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results

    def __call__(self, *args, **kwargs) -> typing.Tuple[Tenant]:
        """Send the request"""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return tuple(Tenant.load(tenant_json) for tenant_json in response.json())


class Count(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('id')
    name = QueryParameter('name')
    name_like = QueryParameter('nameLike')
    user_member = QueryParameter('userMember')
    group_member = QueryParameter('groupMember')
    including_groups_of_user = QueryParameter(
        'includingGroupsOfUser',
        provide=pycamunda.base.value_is_true
    )

    def __init__(
        self,
        url: str,
        id_: str = None,
        name: str = None,
        name_like: str = None,
        user_member: str = None,
        group_member: str = None,
        including_groups_of_user: bool = False
    ):
        """Count tenants.

        :param url: Camunda Rest engine URL.
        :param id_: Filter by the id of the tenant.
        :param name: Filter by the name of the tenant.
        :param name_like: Filter by a substring of the name.
        :param user_member: Filter for tenants where the given user is member of.
        :param group_member: Filter for tenants where  the given group is a member of.
        :param including_groups_of_user: Filter for tenants where the user or one of his groups is a
                                         member of. Can only be used with `user_member` parameter.
        """
        super().__init__(url=url + URL_SUFFIX + '/count')
        self.id_ = id_
        self.name = name
        self.name_like = name_like
        self.user_member = user_member
        self.group_member = group_member
        self.including_groups_of_user = including_groups_of_user

    def __call__(self, *args, **kwargs) -> int:
        """Send the request"""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return response.json()['count']


class Get(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get a tenant.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the tenant.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> Tenant:
        """Send the request"""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return Tenant.load(response.json())


class Create(pycamunda.base.CamundaRequest):

    id_ = BodyParameter('id')
    name = BodyParameter('name')

    def __init__(self, url: str, id_: str, name: str):
        """Create a new tenant.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the tenant.
        :param name: Name of the tenant.
        """
        super().__init__(url=url + URL_SUFFIX + '/create')
        self.id_ = id_
        self.name = name

    def __call__(self, *args, **kwargs) -> None:
        """Send the request"""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)


class Update(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    new_id = BodyParameter('id')
    new_name = BodyParameter('name')

    def __init__(self, url: str, id_: str, new_id: str, new_name: str):
        """Update a tenant.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the tenant.
        :param new_id: New id of the tenant.
        :param new_name: New name of the tenant.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.new_id = new_id
        self.new_name = new_name

    def __call__(self, *args, **kwargs) -> None:
        """Send the request"""
        super().__call__(pycamunda.base.RequestMethod.PUT, *args, **kwargs)


class Options(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str = None):
        """Get a list of options the currently authenticated user can perform on the tenant
        resource.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the tenant.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.id_ = id_

    @property
    def url(self):
        return super().url + (f'/{self.id_}' if self.id_ is not None else '')

    def __call__(self, *args, **kwargs) -> pycamunda.resource.ResourceOptions:
        """Send the request"""
        response = super().__call__(pycamunda.base.RequestMethod.OPTIONS, *args, **kwargs)

        return pycamunda.resource.ResourceOptions.load(response.json())


class Delete(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Delete a tenant.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the tenant.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> None:
        """Send the request"""
        super().__call__(pycamunda.base.RequestMethod.DELETE, *args, **kwargs)
