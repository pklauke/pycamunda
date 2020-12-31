# -*- coding: utf-8 -*-

"""This module provides access to the group REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing

import pycamunda
import pycamunda.resource
import pycamunda.variable
import pycamunda.base
from pycamunda.request import QueryParameter, PathParameter, BodyParameter

URL_SUFFIX = '/group'
URL_SUFFIX_MEMBERS = '/members'


__all__ = [
    'Get', 'GetList', 'Create', 'Update', 'Options', 'Delete', 'MemberCreate', 'MemberDelete',
    'MemberOptions'
]


@dataclasses.dataclass
class Group:
    """Data class of group as returned by the REST api of Camunda."""
    id_: str
    name: str
    type_: str = None

    @classmethod
    def load(cls, data) -> Group:
        group = cls(
            id_=data['id'],
            name=data['name']
        )
        try:
            group.type_ = data['type']
        except KeyError:
            pass

        return group


class Get(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get a group.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the group.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> Group:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return Group.load(response.json())


class GetList(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('id')
    id_in = QueryParameter('idIn')
    name = QueryParameter('name')
    name_like = QueryParameter('nameLike')
    type_ = QueryParameter('type')
    member = QueryParameter('member')
    member_of_tenant = QueryParameter('memberOfTenant')
    sort_by = QueryParameter('sortBy', mapping={'id_': 'id', 'name': 'name', 'type_': 'type'})
    ascending = QueryParameter(
        'sortOrder',
        mapping={True: 'asc', False: 'desc'},
        provide=lambda self, obj, obj_type: vars(obj).get('sort_by', None) is not None
    )
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')

    def __init__(
        self,
        url,
        id_: str = None,
        id_in: typing.Iterable[str] = None,
        name: str = None,
        name_like: str = None,
        type_: str = None,
        member: str = None,
        member_of_tenant: str = None,
        sort_by: str = None,
        ascending: bool = True,
        first_result: int = None,
        max_results: int = None
    ):
        """Get a list of groups.

        :param url: Camunda Rest engine URL.
        :param id_: Filter by the id of the group.
        :param id_in: Filter whether the id of the group is one of multiple ones.
        :param name: Filter by the name of the group.
        :param name_like: Filter by a substring of the name of the group.
        :param type_: Filter by the type of the group.
        :param member: Filter by a member of the group.
        :param member_of_tenant: Filter by member of the tenant.
        :param sort_by: Sort the results by `id_`, `name` or `type_`.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.id_ = id_
        self.id_in = id_in
        self.name = name
        self.name_like = name_like
        self.type_ = type_
        self.member = member
        self.member_of_tenant = member_of_tenant
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results

    def __call__(self, *args, **kwargs) -> typing.Tuple[Group]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return tuple(Group.load(group_json) for group_json in response.json())


class Create(pycamunda.base.CamundaRequest):

    id_ = BodyParameter('id')
    name = BodyParameter('name')
    type_ = BodyParameter('type')

    def __init__(self, url: str, id_: str, name: str, type_: str):
        """Create a new group.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the group.
        :param name: Name of the group.
        :param type_: Type of the group.
        """
        super().__init__(url=url + URL_SUFFIX + '/create')
        self.id_ = id_
        self.name = name
        self.type_ = type_

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)


class Update(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    name = BodyParameter('name')
    type_ = BodyParameter('type')

    def __init__(self, url: str, id_: str, name: str, type_: str):
        """Update a group.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the group.
        :param name: New name of the group.
        :param type_: New zype of the group.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.name = name
        self.type_ = type_

    def body_parameters(self, apply: typing.Callable = ...):
        params = super().body_parameters(apply=apply)
        params['id'] = self.id_
        return params

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.PUT, *args, **kwargs)


class Options(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_=None):
        """Get a list of options the currently authenticated user can perform on the group resource.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.id_ = id_

    @property
    def url(self):
        return super().url + (f'/{self.id_}' if self.id_ is not None else '')

    def __call__(self, *args, **kwargs):
        """Send the request"""
        response = super().__call__(pycamunda.base.RequestMethod.OPTIONS, *args, **kwargs)

        return pycamunda.resource.ResourceOptions.load(response.json())


class Delete(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Delete a group.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the group.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.DELETE, *args, **kwargs)


class MemberCreate(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    user_id = PathParameter('userId')

    def __init__(self, url: str, id_: str, user_id: str):
        """Add a member to a group.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the group.
        :param user_id: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}' + URL_SUFFIX_MEMBERS + '/{userId}')
        self.id_ = id_
        self.user_id = user_id

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.PUT, *args, **kwargs)


class MemberDelete(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    user_id = PathParameter('userId')

    def __init__(self, url: str, id_: str, user_id: str):
        """Delete a member from a group.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the group.
        :param user_id: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}' + URL_SUFFIX_MEMBERS + '/{userId}')
        self.id_ = id_
        self.user_id = user_id

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.DELETE, *args, **kwargs)


class MemberOptions(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get a list of options the currently authenticated user can perform on the group member
        resource.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the group.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}' + URL_SUFFIX_MEMBERS)
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> pycamunda.resource.ResourceOptions:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.OPTIONS, *args, **kwargs)

        return pycamunda.resource.ResourceOptions.load(response.json())
