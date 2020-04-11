# -*- coding: utf-8 -*-

"""This module provides access to the filter REST api of Camunda."""

from __future__ import annotations
import datetime as dt
import dataclasses
import typing

import requests

import pycamunda
import pycamunda.task
import pycamunda.variable
import pycamunda.base
from pycamunda.request import QueryParameter, PathParameter, BodyParameter, BodyParameterContainer

URL_SUFFIX = '/filter'


@dataclasses.dataclass
class Query:

    @classmethod
    def load(cls, **kwargs) -> Query:
        query = cls()
        for key, value in kwargs.items():
            setattr(query, key, value)
        return query


@dataclasses.dataclass
class Properties:

    @classmethod
    def load(cls, **kwargs) -> Properties:
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
    def load(cls, data: typing.Mapping[str, typing.Any]) -> Filter:
        return cls(
            id_=data['id'],
            resource_type=data['resourceType'],
            name=data['name'],
            owner=data['owner'],
            query=Query.load(**data['query']),
            properties=Properties.load(**data['properties']),
            item_count=data.get('itemCount', None)
        )


class GetList(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('filterId')
    resource_type = QueryParameter('resourceType')
    name = QueryParameter('name')
    name_like = QueryParameter('nameLike')
    owner = QueryParameter('owner')
    item_count = QueryParameter('itemCount')
    sort_by = QueryParameter(
        'sortBy',
        mapping={
            'id_': 'filterId',
            'first_name': 'firstName',
            'last_name': 'lastName',
            'email': 'email'
        }
    )
    ascending = QueryParameter(
        'sortOrder',
        mapping={True: 'asc', False: 'desc'},
        provide=lambda self, obj, obj_type: 'sort_by' in vars(obj)
    )
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')

    def __init__(
        self,
        url: str,
        id_: str = None,
        name: str = None,
        name_like: str = None,
        owner: str = None,
        item_count: bool = False,
        sort_by: str = None,
        ascending: bool = True,
        first_result: int = None,
        max_results: int = None
    ):
        """Query for a list of filters using a list of parameters. The size of the result set can be
        retrieved by using the Get Count request.

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
        super().__init__(url=url + URL_SUFFIX)
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

    def send(self) -> typing.Tuple[Filter]:
        """Send the request"""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return tuple(Filter.load(filter_json) for filter_json in response.json())


class Count(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('filterId')
    resource_type = QueryParameter('resourceType')
    name = QueryParameter('name')
    name_like = QueryParameter('nameLike')
    owner = QueryParameter('owner')

    def __init__(
        self,
        url: str,
        id_:str = None,
        name: str = None,
        name_like: str = None,
        owner: str = None
    ):
        """Count filters.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        :param name: Filter by the name of the filter.
        :param name_like: Filter by a substring of the name of the filter.
        :param owner: Filter by the user id of the owner of the filter.
        """
        super().__init__(url=url + URL_SUFFIX + '/count')
        self.id_ = id_
        self.resource_type = 'Task'
        self.name = name
        self.name_like = name_like
        self.owner = owner

    def send(self) -> int:
        """Send the request"""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return response.json()['count']


class Get(pycamunda.base.CamundaRequest):

    id_ = PathParameter('filterId')
    item_count = QueryParameter('itemCount')

    def __init__(self, url: str, id_: str, item_count: bool = False):
        """Query for a filter.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        :param item_count: Return the number of items matched by the respective filter.
        """
        super().__init__(url=url + URL_SUFFIX + '/{filterId}')
        self.id_ = id_
        self.item_count = item_count

    def send(self) -> Filter:
        """Send the request"""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return Filter.load(response.json())


class CriteriaMixin:

    query = BodyParameterContainer('query')

    def add_process_instance_criteria(
        self,
        id_: str = ...,
        business_key: str = ...,
        business_key_like: str = ...
    ):
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

    def add_process_definition_criteria(
        self,
        id_: str = ...,
        key: str = ...,
        key_in: typing.Iterable[str] = ...,
        name: str = ...,
        name_like: str = ...
    ):
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

    def add_case_instance_criteria(
        self,
        id_: str = ...,
        business_key: str = ...,
        business_key_like: str = ...
    ):
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

    def add_case_definition_criteria(
        self,
        id_: str = ...,
        key: str = ...,
        name: str = ...,
        name_like: str = ...
    ):
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

    def add_other_criteria(
        self,
        active: bool = ...,
        activity_instance_id_in: typing.Iterable[str] = ...,
        execution_id: str = ...
    ):
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

    def add_user_criteria(
        self,
        assignee: str = ...,
        assignee_in: typing.Iterable[str] = ...,
        assignee_like: str = ...,
        owner: str = ...,
        candidate_group: str = ...,
        candidate_groups: typing.Iterable[str] = ...,
        candidate_user: str = ...,
        involved_user: str = ...,
        unassigned: bool = ...,
        delegation_state: typing.Union[str, pycamunda.task.DelegationState] = ...
    ):
        """Add criteria that filter by user.

        :param assignee: Filter by the assignee of the task.
        :param assignee_in: Filter whether assignee of the task is one of multiple ones.
        :param assignee_like: Filter by a substring of the assignee of the task.
        :param owner: Filter by the owner of the task.
        :param candidate_group: Filter by the candidate group of the task.
        :param candidate_groups: Filter whether the candidate group of the task is one of multiple
                                 ones.
        :param candidate_user: Filter by the candidate user of the task.
        :param involved_user: TODO
        :param unassigned: Filter only unassigned tasks.
        :param delegation_state: Filter by delegation state.
        """
        if candidate_user is not Ellipsis and (
                candidate_group is not Ellipsis or candidate_groups is not Ellipsis):
            raise pycamunda.PyCamundaException(
                'candidate user and candidate groups must not be both provided.'
            )

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
        if delegation_state is not Ellipsis:
            self.query.parameters['delegationState'] = None
            if delegation_state is not None:
                self.query.parameters['delegationState'] = pycamunda.task.DelegationState(
                    delegation_state
                )
        return self

    def add_task_criteria(
        self,
        definition_key: str = ...,
        definition_key_in: typing.Iterable[str] = ...,
        definition_key_like: str = ...,
        name: str = ...,
        name_like: str = ...,
        description: str = ...,
        description_like: str = ...,
        priority: int = ...,
        max_priority: int = ...,
        min_priority: int = ...,
        tenant_id_in: typing.Iterable[str] = ...,
        without_tenant_id: bool = False
    ):
        """Add criteria that filter by task.

        :param definition_key: Filter by the definition key of the task.
        :param definition_key_in: Filter whether definition key of the task is one of multiple ones.
        :param definition_key_like: Filter by a substring of the definition key of the task.
        :param name: Filter by the name of the task.
        :param name_like:  Filter by a substring of the name of the task.
        :param description: Filter by the description of the task.
        :param description_like: Filter by a substring of the description of the task.
        :param priority: Filter by the priority of the task.
        :param max_priority: Filter by a maximum priority of the task.
        :param min_priority: Filter by a minimum priority of the task.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Filter only tasks without tenant id.
        """
        if definition_key is not Ellipsis:
            self.query.parameters['taskDefinitionKey'] = definition_key
        if definition_key_in is not Ellipsis:
            self.query.parameters['taskDefinitionKeyIn'] = definition_key_in
        if definition_key_like is not Ellipsis:
            self.query.parameters['taskDefinitionKeyLike'] = definition_key_like
        if name is not Ellipsis:
            self.query.parameters['name'] = name
        if name_like is not Ellipsis:
            self.query.parameters['nameLike'] = name_like
        if description is not Ellipsis:
            self.query.parameters['description'] = description
        if description_like is not Ellipsis:
            self.query.parameters['descriptionLike'] = description_like
        if priority is not Ellipsis:
            self.query.parameters['priority'] = priority
        if max_priority is not Ellipsis:
            self.query.parameters['maxPriority'] = max_priority
        if min_priority is not Ellipsis:
            self.query.parameters['minPriority'] = min_priority
        if tenant_id_in is not Ellipsis:
            self.query.parameters['tenantIdIn'] = tenant_id_in
        self.query.parameters['withoutTenantId'] = without_tenant_id

        return self

    def add_datetime_criteria(
        self,
        created_before: dt.datetime = ...,
        created_after: dt.datetime = ...,
        due_before: dt.datetime = ...,
        due_after: dt.datetime = ...,
        follow_up_after: dt.datetime = ...,
        follow_up_before: dt.datetime = ...,
        follow_up_before_or_not_existent: dt.datetime = ...
    ):
        """Add criteria that filter by datetime. Datetime objects are expected to contain timezone
        information.

        :param created_before: Filter by tasks that were created before the given date.
        :param created_after: Filter by tasks that were created after the given date.
        :param due_before: Filter by tasks where due date has already passed at given date.
        :param due_after: Filter by tasks where due date has not passed at given date.
        :param follow_up_after: Filter by tasks that have a follow up date that has not passed yet
                                at given date.
        :param follow_up_before: Filter by tasks that have a follow up date that has already passed
                                 at given date.
        :param follow_up_before_or_not_existent: Filter by tasks that do not have a follow up date
                                                 or one that has already passed.
        """
        if created_before is not Ellipsis:
            self.query.parameters['createdBefore'] = created_before
        if created_after is not Ellipsis:
            self.query.parameters['createdAfter'] = created_after
        if due_before is not Ellipsis:
            self.query.parameters['dueBefore'] = due_before
        if due_after is not Ellipsis:
            self.query.parameters['dueAfter'] = due_after
        if follow_up_after is not Ellipsis:
            self.query.parameters['followUpAfter'] = follow_up_after
        if follow_up_before is not Ellipsis:
            self.query.parameters['followUpBefore'] = follow_up_before
        if follow_up_before_or_not_existent is not Ellipsis:
            self.query.parameters['followUpBeforeOrNotExistent'] = follow_up_before_or_not_existent

        return self


class Create(pycamunda.base.CamundaRequest, CriteriaMixin):

    resource_type = BodyParameter('resourceType')
    name = BodyParameter('name')
    owner = BodyParameter('owner')
    query = BodyParameterContainer('query')  # TODO test if this can be removed
    properties = BodyParameterContainer('properties')

    def __init__(self, url: str, name: str, owner: str = None):
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

    def send(self) -> Filter:
        """Send the request"""
        params = self.body_parameters()
        try:
            response = requests.post(self.url, json=params)
        except requests.exceptions.RequestException as exc:
            raise pycamunda.PyCamundaException(exc)
        if not response:
            pycamunda.base._raise_for_status(response)

        return Filter.load(response.json())


class Update(pycamunda.base.CamundaRequest, CriteriaMixin):

    id_ = PathParameter('id')
    resource_type = BodyParameter('resourceType')
    name = BodyParameter('name')
    owner = BodyParameter('owner')
    query = BodyParameterContainer('query')  # TODO test if this can be removed
    properties = BodyParameterContainer('properties')

    def __init__(self, url: str, id_: str, name: str = None, owner: str = None):
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

    def add_properties(self, **kwargs):
        for key, value in kwargs.items():
            self.properties.parameters[key] = value

        return self

    def send(self) -> None:
        """Send the request"""
        params = self.body_parameters()
        try:
            response = requests.put(self.url, json=params)
        except requests.exceptions.RequestException as exc:
            raise pycamunda.PyCamundaException(exc)
        if not response:
            pycamunda.base._raise_for_status(response)


class Delete(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Delete a filter.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def send(self):
        """Send the request."""
        try:
            response = requests.delete(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)


class Execute(pycamunda.base.CamundaRequest, CriteriaMixin):

    id_ = PathParameter('id')
    query = BodyParameterContainer('query')  # TODO test if this can be removed

    def __init__(self, url: str, id_: str, single_result: bool = False):
        """Execute a filter.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.single_result = single_result

    def send(self) -> typing.Union[pycamunda.task.Task, typing.Tuple[pycamunda.task.Task]]:
        """Send the request."""
        params = self.body_parameters()['query']
        url = self.url + ('/singleResult' if self.single_result else '/list')
        try:
            if params:
                response = requests.post(url, json=params)
            else:
                response = requests.get(url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        if self.single_result:
            return pycamunda.task.Task.load(response.json())
        return tuple(pycamunda.task.Task.load(task_json) for task_json in response.json())


class ExecuteCount(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get the number of results returned by executing a filter.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/count')
        self.id_ = id_

    def send(self) -> int:
        """Send the request."""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return response.json()['count']
