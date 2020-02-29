# -*- coding: utf-8 -*-

"""This module provides access to the filter REST api of Camunda."""

import requests
import dataclasses
import typing

import pycamunda
import pycamunda.request
from pycamunda.request import PathParameter, QueryParameter, BodyParameter, BodyParameterContainer

URL_SUFFIX = '/filter'


@dataclasses.dataclass
class Query:

    @classmethod
    def load(cls, **kwargs):
        query = cls()
        for key, value in kwargs.items():
            setattr(query, key, value)
        return query


@dataclasses.dataclass
class Properties:

    @classmethod
    def load(cls, **kwargs):
        properties = cls()
        for key, value in kwargs.items():
            setattr(properties, key, value)
        return properties


@dataclasses.dataclass
class Filter:
    id_: str
    resource_type: str
    name: str
    owner: str
    query: Query
    properties: Properties
    item_count: int = None

    @classmethod
    def load(cls, data):
        return Filter(
            id_=data['id'],
            resource_type=data['resourceType'],
            name=data['name'],
            owner=data['owner'],
            query=Query.load(**data['query']),
            properties=Properties.load(**data['properties']),
            item_count=data.get('itemCount', None)
        )


class GetList(pycamunda.request.CamundaRequest):

    id_ = QueryParameter('filterId')
    resource_type = QueryParameter('resourceType')
    name = QueryParameter('name')
    name_like = QueryParameter('nameLike')
    owner = QueryParameter('owner')
    item_count = QueryParameter('itemCount')
    sort_by = QueryParameter('sortBy')
    ascending = QueryParameter('sortOrder', mapping={True: 'asc', False: 'desc'},
                               provide=lambda self: 'sort_by' in vars(self))
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')

    def __init__(self, url, id_=None, resource_type=None, name=None, name_like=None, owner=None,
                 item_count=False, sort_by=None, ascending=True, first_result=None,
                 max_results=None):
        """Query for a list of filters using a list of parameters. The size of the result set can be
        retrieved by using the Get Filter Count method.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        :param resource_type: Filter by the resource type of the filter.
        :param name: Filter by the name of the filter.
        :param name_like: Filter by a substring of the name of the filter.
        :param owner: Filter by the user id of the owner of the filter.
        :param item_count: Return the number of items matched by the respective filters.
        :param sort_by: Sort the results by `id_`, `first_name`, `last_name` or `email` of the user.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url + URL_SUFFIX)
        self.id_ = id_
        self.resource_type = resource_type
        self.name = name
        self.name_like = name_like
        self.owner = owner
        self.item_count = item_count
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results

    def send(self):
        """Send the request"""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return tuple(Filter.load(filter_json) for filter_json in response.json())


class Count(pycamunda.request.CamundaRequest):

    id_ = QueryParameter('filterId')
    resource_type = QueryParameter('resourceType')
    name = QueryParameter('name')
    name_like = QueryParameter('nameLike')
    owner = QueryParameter('owner')

    def __init__(self, url, id_=None, resource_type=None, name=None, name_like=None, owner=None):
        """Count filters.1

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        :param resource_type: Filter by the resource type of the filter.
        :param name: Filter by the name of the filter.
        :param name_like: Filter by a substring of the name of the filter.
        :param owner: Filter by the user id of the owner of the filter.
        """
        super().__init__(url + URL_SUFFIX + '/count')
        self.id_ = id_
        self.resource_type = resource_type
        self.name = name
        self.name_like = name_like
        self.owner = owner

    def send(self):
        """Send the request"""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        print(response.json())
        return response.json()['count']


class Get(pycamunda.request.CamundaRequest):

    id_ = PathParameter('filterId')
    item_count = QueryParameter('itemCount')

    def __init__(self, url, id_, item_count=False):
        """Query for a filter.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        :param item_count: Return the number of items matched by the respective filter.
        """
        super().__init__(url + URL_SUFFIX + '/{filterId}')
        self.id_ = id_
        self.item_count = item_count

    def send(self):
        """Send the request"""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return Filter.load(response.json())


class Create(pycamunda.request.CamundaRequest):

    resource_type = BodyParameter('resourceType')
    name = BodyParameter('name')
    owner = BodyParameter('owner')
    query = BodyParameterContainer('query')
    properties = BodyParameterContainer('properties')

    def __init__(self, url, resource_type=None, name=None, owner=None):
        """Create a new filter.

        :param url: Camunda Rest engine URL.
        :param resource_type: Resource type of the filter.
        :param name: Name of the filter.
        :param owner: User id of the owner of the filter.
        """
        super().__init__(url=url + URL_SUFFIX + '/create')
        self.resource_type = resource_type
        self.name = name
        self.owner = owner

    def add_query(self, **kwargs):
        for key, value in kwargs.items():
            self.query.parameters[key] = value

    def add_properties(self, **kwargs):
        for key, value in kwargs.items():
            self.properties.parameters[key] = value

    def send(self):
        """Send the request"""
        params = self.body_parameters()
        try:
            response = requests.post(self.url, json=params)
        except requests.exceptions.RequestException as exc:
            raise pycamunda.PyCamundaException(exc)
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return Filter.load(response.json())


class Update(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')
    resource_type = BodyParameter('resourceType')
    name = BodyParameter('name')
    owner = BodyParameter('owner')
    query = BodyParameterContainer('query')
    properties = BodyParameterContainer('properties')

    def __init__(self, url, id_, resource_type=None, name=None, owner=None):
        """Update a filter.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        :param resource_type: Resource type of the filter.
        :param name: Name of the filter.
        :param owner: User id of the owner of the filter.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.resource_type = resource_type
        self.name = name
        self.owner = owner

    def add_query(self, **kwargs):
        for key, value in kwargs.items():
            self.query.parameters[key] = value

    def add_properties(self, **kwargs):
        for key, value in kwargs.items():
            self.properties.parameters[key] = value

    def send(self):
        """Send the request"""
        params = self.body_parameters()
        try:
            response = requests.put(self.url, json=params)
        except requests.exceptions.RequestException as exc:
            raise pycamunda.PyCamundaException(exc)
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)


class Delete(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url, id_):
        """Delete a filter.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        """
        super().__init__(url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def send(self):
        """Send the request."""
        try:
            response = requests.delete(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)