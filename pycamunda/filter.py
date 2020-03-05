# -*- coding: utf-8 -*-

"""This module provides access to the filter REST api of Camunda."""

import requests
import dataclasses

import pycamunda
import pycamunda.request
from pycamunda.request import PathParameter, QueryParameter, BodyParameter, BodyParameterContainer
import pycamunda.task

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

    def __init__(self, url, id_=None, name=None, name_like=None, owner=None,
                 item_count=False, sort_by=None, ascending=True, first_result=None,
                 max_results=None):
        """Query for a list of filters using a list of parameters. The size of the result set can be
        retrieved by using the Get Filter Count method.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
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
        self.resource_type = 'Task'
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

    def __init__(self, url, id_=None, name=None, name_like=None, owner=None):
        """Count filters.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        :param name: Filter by the name of the filter.
        :param name_like: Filter by a substring of the name of the filter.
        :param owner: Filter by the user id of the owner of the filter.
        """
        super().__init__(url + URL_SUFFIX + '/count')
        self.id_ = id_
        self.resource_type = 'Task'
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


class CriteriaMixin:

    query = BodyParameterContainer('query')

    def add_process_instance_criteria(self, id_=..., business_key=..., business_key_like=...):
        """Add criteria that filter by process instance.

        :param id_: Filter by the id of the process instance.
        :param business_key: Filter by the business key of the process instance.
        :param business_key_like: Filter by a substring of the business key of the filter.
        """
        if id_ is not Ellipsis:
            self.query.parameters['processInstanceId'] = id_
        if business_key is not Ellipsis:
            self.query.parameters['processInstanceBusinessKey'] = business_key
        if business_key_like is not Ellipsis:
            self.query.parameters['processInstanceBusinessKeyLike'] = business_key_like

        return self

    def add_process_definition_criteria(self, id_=..., key=..., key_in=..., name=...,
                                        name_like=...):
        """Add criteria that filter by the process definition.

        :param id_: Filter by the id of the process definition.
        :param key: Filter by the key of the process definition.
        :param key_in: Filter by a substring of the key of the process definition.
        :param name: Filter by the name of the process definition.
        :param name_like: Filter by a substring of the name of the process definition.
        """
        if id_ is not Ellipsis:
            self.query.parameters['processDefinitionId'] = id_
        if key is not Ellipsis:
            self.query.parameters['processDefinitionKey'] = key
        if key_in is not Ellipsis:
            self.query.parameters['processDefinitionKeyIn'] = key_in
        if name is not Ellipsis:
            self.query.parameters['processDefinitionName'] = name
        if name_like is not Ellipsis:
            self.query.parameters['processDefinitionNameLike'] = name_like

        return self

    def add_case_instance_criteria(self, id_=..., business_key=..., business_key_like=...):
        """Add criteria that filter by the case instance.

        :param id_: Filter by the id of the case instance.
        :param business_key: Filter by the business key of the case instance.
        :param business_key_like: Filter by a substring of the business key of the case instance.
        """
        if id_ is not Ellipsis:
            self.query.parameters['caseInstanceId'] = id_
        if business_key is not Ellipsis:
            self.query.parameters['caseInstanceBusinessKey'] = business_key
        if business_key_like is not Ellipsis:
            self.query.parameters['caseInstanceBusinessKeyLike'] = business_key_like

        return self

    def add_case_definition_criteria(self, id_=..., key=..., name=..., name_like=...):
        """Add criteria that filter by the case definition.

        :param id_: Filter by the id of the case definition.
        :param key: Filter by the key of the case definition.
        :param name: Filter by the name of the case definition.
        :param name_like: Filter by a substring of the name of the case definition.
        """
        if id_ is not Ellipsis:
            self.query.parameters['caseDefinitionId'] = id_
        if key is not Ellipsis:
            self.query.parameters['caseDefinitionKey'] = key
        if name is not Ellipsis:
            self.query.parameters['caseDefinitionName'] = name
        if name_like is not Ellipsis:
            self.query.parameters['caseDefinitionNameLike'] = name_like

    def add_other_criteria(self, active=..., activity_instance_id_in=..., execution_id=...):
        """Add criteria that filter by active status, activity instance or execution id.

        :param active: Filter only active tasks.
        :param activity_instance_id_in: Filter by activity instance ids.
        :param execution_id: Filter by the execution id.
        """
        if active is not Ellipsis:
            self.query.parameters['active'] = active or None
        if activity_instance_id_in is not Ellipsis:
            self.query.parameters['activityInstanceIdIn'] = activity_instance_id_in
        if execution_id is not Ellipsis:
            self.query.parameters['executionId'] = execution_id

    def add_user_criteria(self, assignee=..., assignee_in=..., assignee_like=..., owner=...,
                          candidate_group=..., candidate_groups=..., candidate_user=...,
                          involved_user=..., unassigned=..., delegation_resolved=...):
        """Add criteria that filter by user.

        :param assignee: Filter by the assignee of the task.
        :param assignee_in: Filter whether assignee of the task is one multiple ones.
        :param assignee_like: Filter by a substring of the assignee of the task.
        :param owner: Filter by the owner of the task.
        :param candidate_group: Filter by the candidate group of the task.
        :param candidate_groups: Filter whether the candidate group of the task is one of multiple
                                 ones.
        :param candidate_user: Filter by the candidate user of the task.
        :param involved_user: TODO
        :param unassigned: Filter only unassigned tasks.
        :param delegation_resolved: Filter by delegation state.
        """
        if candidate_user is not Ellipsis and (
                candidate_group is not Ellipsis or candidate_groups is not Ellipsis):
            raise pycamunda.PyCamundaInvalidInput('candidate user and candidate groups must not be '
                                                  'both provided.')

        if assignee is not Ellipsis:
            self.query.parameters['assignee'] = assignee
        if assignee_in is not Ellipsis:
            self.query.parameters['assigneeIn'] = assignee_in
        if assignee_like is not Ellipsis:
            self.query.parameters['assigneeLike'] = assignee_like
        if owner is not Ellipsis:
            self.query.parameters['owner'] = owner
        if candidate_group is not Ellipsis:
            self.query.parameters['candidateGroup'] = candidate_group
        if candidate_groups is not Ellipsis:
            self.query.parameters['candidateGroups'] = candidate_groups
        if candidate_user is not Ellipsis:
            self.query.parameters['candidateUser'] = candidate_user
        if involved_user is not Ellipsis:
            self.query.parameters['involvedUser'] = involved_user
        if unassigned is not Ellipsis:
            self.query.parameters['unassigned'] = unassigned
        if delegation_resolved is None:
            self.query.parameters['delegationState'] = None
        elif delegation_resolved is not Ellipsis:
            self.query.parameters['delegationState'] = \
                'RESOLVED' if delegation_resolved else 'PENDING'

        return self


class Create(pycamunda.request.CamundaRequest, CriteriaMixin):

    resource_type = BodyParameter('resourceType')
    name = BodyParameter('name')
    owner = BodyParameter('owner')
    query = BodyParameterContainer('query')
    properties = BodyParameterContainer('properties')

    def __init__(self, url, name, owner=None):
        """Create a new filter.

        :param url: Camunda Rest engine URL.
        :param name: Name of the filter.
        :param owner: User id of the owner of the filter.
        """
        super().__init__(url=url + URL_SUFFIX + '/create')
        self.resource_type = 'Task'
        self.name = name
        self.owner = owner

    def add_query(self, **kwargs):
        for key, value in kwargs.items():
            self.query.parameters[key] = value

        return self

    def add_properties(self, **kwargs):
        for key, value in kwargs.items():
            self.properties.parameters[key] = value

        return self

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

    def __init__(self, url, id_, name=None, owner=None):
        """Update a filter.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        :param name: Name of the filter.
        :param owner: User id of the owner of the filter.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.resource_type = 'Task'
        self.name = name
        self.owner = owner

    def add_query(self, **kwargs):
        for key, value in kwargs.items():
            self.query.parameters[key] = value

        return self

    def add_properties(self, **kwargs):
        for key, value in kwargs.items():
            self.properties.parameters[key] = value

        return self

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


class Execute(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')
    query = BodyParameterContainer('query')

    def __init__(self, url, id_, single_result=False):
        """Execute a filter.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        """
        super().__init__(url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.single_result = single_result

    def send(self):
        """Send the request."""
        try:
            response = requests.get(self.url + ('/singleResult' if self.single_result else '/list'))
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        if self.single_result:
            return pycamunda.task.Task.load(response.json())
        return tuple(pycamunda.task.Task.load(task_json) for task_json in response.json())


class ExecuteCount(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url, id_):
        """Get the number of results returned by executing a filter.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        """
        super().__init__(url + URL_SUFFIX + '/{id}/count')
        self.id_ = id_

    def send(self):
        """Send the request."""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return response.json()['count']
