# -*- coding: utf-8 -*-

"""This module provides access to the auth REST api of Camunda."""

from __future__ import annotations
import typing
import dataclasses
import enum
import datetime as dt

import pycamunda
import pycamunda.base
import pycamunda.resource
from pycamunda.request import QueryParameter, PathParameter, BodyParameter

URL_SUFFIX = '/auth'


__all__ = ['AuthorizationType', 'GetList', 'Count', 'Get', 'Check', 'Options', 'Update', 'Create',
           'Delete']


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
    links: typing.Tuple[pycamunda.resource.Link] = None
    root_process_instance_id: str = None
    removal_time: dt.datetime = None

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> Authorization:
        authorization = cls(
            id_=data['id'],
            type_=data['type'],
            permissions=data['permissions'],
            user_id=data['userId'],
            group_id=data['groupId'],
            resource_type=pycamunda.resource.ResourceType(data['resourceType']),
            resource_id=data['resourceId']
        )
        try:
            authorization.links = tuple(
                pycamunda.resource.Link.load(data=link) for link in data['links']
            )
        except KeyError:
            pass
        try:
            authorization.removal_time = pycamunda.base.from_isoformat(data['removalTime'])
        except KeyError:
            pass
        try:
            authorization.root_process_instance_id = data['rootProcessInstanceId']
        except KeyError:
            pass

        return authorization


@dataclasses.dataclass
class Permission:
    """Data class of permission as returned by the REST api of Camunda."""
    permission_name: str
    resource_name: str
    resource_id: str
    authorized: bool

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> Permission:
        return cls(
            permission_name=data['permissionName'],
            resource_name=data['resourceName'],
            resource_id=data['resourceId'],
            authorized=data['authorized']
        )


class GetList(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('id')
    type_ = QueryParameter('type')
    user_id_in = QueryParameter('userIdIn')
    group_id_in = QueryParameter('groupIdIn')
    resource_type = QueryParameter('resourceType')
    resource_id = QueryParameter('resourceId')
    sort_by = QueryParameter(
        'sortBy',
        mapping={
            'resource_type': 'resourceType',
            'resource_id': 'resourceId'
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
        type_: typing.Union[str, AuthorizationType] = None,
        user_id_in: typing.Iterable[str] = None,
        group_id_in: typing.Iterable[str] = None,
        resource_type: typing.Union[str, pycamunda.resource.ResourceType] = None,
        resource_id: int = None,
        sort_by: str = None,
        ascending: bool = True,
        first_result: int = None,
        max_results: int = None
    ):
        """Query for a list of authorizations using a list of parameters. The size of the result set
        can be retrieved by using the Get Count request.

        :param url: Camunda Rest engine URL.
        :param id_: Filter by the id of the authorization.
        :param type_: Filter by the authorization type.
        :param user_id_in: Filter whether the user id is one of multiple ones.
        :param group_id_in: Filter whether the group id is one of multiple ones.
        :param resource_type: Filter by the resource type.
        :param resource_id: Filter by the resource id.
        :param sort_by: Sort the results by `id_`, `lock_expiration_time, `process_instance_id`,
                        `process_definition_key`, `tenant_id` or `task_priority`.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.id_ = id_
        self.type_ = None
        if type_ is not None:
            self.type_ = AuthorizationType(type_)
        self.user_id_in = user_id_in
        self.group_id_in = group_id_in
        self.resource_type = None
        if type_ is not None:
            self.resource_type = pycamunda.resource.ResourceType(resource_type)
        self.resource_id = resource_id
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results

    def __call__(self, *args, **kwargs) -> typing.Tuple[Authorization]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return tuple(Authorization.load(auth_json) for auth_json in response.json())


class Count(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('id')
    type_ = QueryParameter('type')
    user_id_in = QueryParameter('userIdIn')
    group_id_in = QueryParameter('groupIdIn')
    resource_type = QueryParameter('resourceType')
    resource_id = QueryParameter('resourceId')

    def __init__(
        self,
        url: str,
        id_: str = None,
        type_: typing.Union[str, AuthorizationType] = None,
        user_id_in: typing.Iterable[str] = None,
        group_id_in: typing.Iterable[str] = None,
        resource_type: typing.Union[str, pycamunda.resource.ResourceType] = None,
        resource_id: int = None,
    ):
        """Get the size of the result returned by the Get List request.

        :param url: Camunda Rest engine URL.
        :param id_: Filter by the id of the authorization.
        :param type_: Filter by the authorization type.
        :param user_id_in: Filter whether the user id is one of multiple ones.
        :param group_id_in: Filter whether the group id is one of multiple ones.
        :param resource_type: Filter by the resource type.
        :param resource_id: Filter by the resource id.
        """
        super().__init__(url=url + URL_SUFFIX + '/count')
        self.id_ = id_
        self.type_ = None
        if type_ is not None:
            self.type_ = AuthorizationType(type_)
        self.user_id_in = user_id_in
        self.group_id_in = group_id_in
        self.resource_type = None
        if type_ is not None:
            self.resource_type = pycamunda.resource.ResourceType(resource_type)
        self.resource_id = resource_id

    def __call__(self, *args, **kwargs) -> int:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return int(response.json()['count'])


class Get(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get an auth.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the authorization.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> Authorization:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return Authorization.load(data=response.json())


class Check(pycamunda.base.CamundaRequest):

    permission_name = QueryParameter('permissionName')
    permission_value = QueryParameter('permissionValue')
    resource_name = QueryParameter('resourceName')
    resource_type = QueryParameter('resourceType')
    resource_id = QueryParameter('resourceId')

    def __init__(
        self,
        url: str,
        permission_name: str,
        permission_value: int,
        resource_name: str,
        resource_type: typing.Union[str, pycamunda.resource.ResourceType],
        resource_id: str = None
    ):
        """Check the authorization of the currently authenticated user.

        :param url: Camunda Rest engine URL.
        :param permission_name: Name of the permission to check.
        :param permission_value: Value of the permission to check for.
        :param resource_name: Name of the resource to check for.
        :param resource_type: Type of the resource to check for.
        :param resource_id: Id of the resource to check for.
        """
        super().__init__(url=url + URL_SUFFIX + '/check')
        self.permission_name = permission_name
        self.permission_value = permission_value
        self.resource_name = resource_name
        self.resource_type = resource_type
        self.resource_id = resource_id

    def __call__(self, *args, **kwargs) -> Permission:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return Permission.load(data=response.json())


class Options(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str = None):
        """Get a list of options the currently authenticated user can perform on the authorization
        resource.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the authorization
        """
        super().__init__(url=url + URL_SUFFIX + '{path}')
        self.id_ = id_

    @property
    def url(self):
        return self._url.format(path='/{id}'.format(id=self.id_) if self.id_ is not None else '')

    def __call__(self, *args, **kwargs) -> pycamunda.resource.ResourceOptions:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.OPTIONS, *args, **kwargs)

        return pycamunda.resource.ResourceOptions.load(data=response.json())


class Create(pycamunda.base.CamundaRequest):

    type_ = BodyParameter('type')
    permissions = BodyParameter('permissions')
    user_id = BodyParameter('userId')
    group_id = BodyParameter('groupId')
    resource_type = BodyParameter('resourceType')
    resource_id = BodyParameter('resourceId')

    def __init__(
        self,
        url: str,
        type_: typing.Union[int, AuthorizationType],
        permissions: typing.Iterable[str],
        resource_type: typing.Union[str, pycamunda.resource.ResourceType],
        resource_id: str,
        user_id: str = None,
        group_id: str = None
    ):
        """Create an auth.

        :param url: Camunda Rest engine URL.
        :param type_: Id of the authorization.
        :param permissions: Permissions provided by this authorization. A permission be 'READ' or
                            'CREATE' for example.
        :param user_id: Id of the user this authorization is for. The value '*' means all users.
        :param group_id: Id of the group this authorization is for.
        :param resource_type: Resource type this authorization is for.
        :param resource_id: Id of the resource. The value '*' means all instances of a resource.
        """
        super().__init__(url=url + URL_SUFFIX + '/create')
        self.type_ = type_
        self.permissions = permissions
        self.user_id = user_id
        self.group_id = group_id
        self.resource_type = resource_type
        self.resource_id = resource_id

    def __call__(self, *args, **kwargs) -> Authorization:
        """Send the request."""
        assert (self.user_id is not None) != (self.group_id is not None), (
            'Either \'user_id\' or \'group_id\' has to be provided, not both.'
        )
        response = super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)

        return Authorization.load(data=response.json())


class Update(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    permissions = BodyParameter('permissions')
    user_id = BodyParameter('userId')
    group_id = BodyParameter('groupId')
    resource_type = BodyParameter('resourceType')
    resource_id = BodyParameter('resourceId')

    def __init__(
        self,
        url: str,
        id_: str,
        permissions: typing.Iterable[str],
        resource_type: typing.Union[str, pycamunda.resource.ResourceType],
        resource_id: str,
        user_id: str = None,
        group_id: str = None
    ):
        """Update an auth.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the authorization.
        :param permissions: Permissions provided by this authorization. A permission be 'READ' or
                            'CREATE' for example.
        :param user_id: Id of the user this authorization is for. The value '*' means all users.
        :param group_id: Id of the group this authorization is for.
        :param resource_type: Resource type this authorization is for.
        :param resource_id: Id of the resource. The value '*' means all instances of a resource.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.permissions = permissions
        self.user_id = user_id
        self.group_id = group_id
        self.resource_type = resource_type
        self.resource_id = resource_id

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        assert (self.user_id is not None) != (self.group_id is not None), (
            'Either \'user_id\' or \'group_id\' has to be provided, not both.'
        )
        super().__call__(pycamunda.base.RequestMethod.PUT, *args, **kwargs)


class Delete(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Delete an auth.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the authorization.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.DELETE, *args, **kwargs)
