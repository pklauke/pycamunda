# -*- coding: utf-8 -*-

"""This module provides access to the group REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing

import requests

import pycamunda
import pycamunda.request
from pycamunda.request import PathParameter, QueryParameter, BodyParameter


URL_SUFFIX = '/group'


@dataclasses.dataclass
class Group:
    id_: str
    name: str
    type_: str

    @classmethod
    def load(cls, data):
        return cls(
            id_=data['id'],
            name=data['name'],
            type_=data['type']
        )


class Get(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get a group.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the group.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def send(self) -> Group:
        """Send the request."""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return Group.load(response.json())


class GetList(pycamunda.request.CamundaRequest):

    id_ = QueryParameter('id')
    id_in = QueryParameter('idIn')
    name = QueryParameter('name')
    name_like = QueryParameter('nameLike')
    type_ = QueryParameter('type')
    member = QueryParameter('member')
    member_of_tenant = QueryParameter('memberOfTenant')
    sort_by = QueryParameter('sortBy', mapping={'id_': 'id', 'name': 'name', 'type_': 'type'})
    ascending = QueryParameter('sortOrder', mapping={True: 'asc', False: 'desc'},
                               provide=lambda self, obj, obj_type: 'sort_by' in vars(self))
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

    def send(self) -> typing.Tuple[Group]:
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return tuple(Group.load(group_json) for group_json in response.json())


class Create(pycamunda.request.CamundaRequest):

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

    def send(self) -> None:
        """Send the request."""
        params = self.body_parameters()
        try:
            response = requests.post(self.url, json=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)


class Update(pycamunda.request.CamundaRequest):

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

    def send(self) -> None:
        """Send the request."""
        params = self.body_parameters()
        params['id'] = self.id_
        try:
            response = requests.put(self.url, json=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)


class Options(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url, id_=None):
        """Get a list of options the currently authenticated user can perform on the group resource.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def send(self):
        """Send the request"""
        try:
            response = requests.options(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return pycamunda.ResourceOptions.load(response.json())


class Delete(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Delete a group.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the group.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def send(self) -> None:
        """Send the request."""
        try:
            response = requests.delete(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)
