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
    """Data class of query."""

    @classmethod
    def load(cls, **kwargs) -> Query:
        query = cls()
        for key, value in kwargs.items():
            setattr(query, key, value)
        return query


@dataclasses.dataclass
class Properties:
    """Data class of properties."""

    @classmethod
    def load(cls, **kwargs) -> Properties:
        properties = cls()
        for key, value in kwargs.items():
            setattr(properties, key, value)
        return properties


@dataclasses.dataclass
class Filter:
    """Data class of filter as returned by the REST api of Camunda."""
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

    def __call__(self, *args, **kwargs) -> typing.Tuple[Filter]:
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

    def __call__(self, *args, **kwargs) -> int:
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

    def __call__(self, *args, **kwargs) -> Filter:
        """Send the request"""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return Filter.load(response.json())


class _Criteria(pycamunda.request.Request):

    process_instance_id = BodyParameter('processInstanceId')
    process_instance_business_key = BodyParameter('processInstanceBusinessKey')
    process_instance_business_key_like = BodyParameter('processInstanceBusinessKeyLike')
    process_definition_id = BodyParameter('processDefinitionId')
    process_definition_key = BodyParameter('processDefinitionKey')
    process_definition_key_in = BodyParameter('processDefinitionKeyIn')
    process_definition_name = BodyParameter('processDefinitionName')
    process_definition_name_like = BodyParameter('processDefinitionNameLike')
    case_instance_id = BodyParameter('caseInstanceId')
    case_instance_business_key = BodyParameter('caseInstanceBusinessKey')
    case_instance_business_key_like = BodyParameter('caseInstanceBusinessKeyLike')
    case_definition_id = BodyParameter('caseDefinitionId')
    case_definition_key = BodyParameter('caseDefinitionKey')
    case_definition_name = BodyParameter('caseDefinitionName')
    case_definition_name_like = BodyParameter('caseDefinitionNameLike')
    active = BodyParameter('active')
    activity_instance_id_in = BodyParameter('activityInstanceIdIn')
    execution_id = BodyParameter('executionId')
    assignee = BodyParameter('assignee')
    assignee_in = BodyParameter('assigneeIn')
    assignee_like = BodyParameter('assigneeLike')
    task_owner = BodyParameter('owner')
    candidate_group = BodyParameter('candidateGroup')
    candidate_groups = BodyParameter('candidateGroups')
    candidate_user = BodyParameter('candidateUser')
    involved_user = BodyParameter('involvedUser')
    unassigned = BodyParameter('unassigned')
    delegation_state = BodyParameter('delegationState')
    task_definition_key = BodyParameter('taskDefinitionKey')
    task_definition_key_in = BodyParameter('taskDefinitionKeyIn')
    task_definition_key_like = BodyParameter('taskDefinitionKeyLike')
    task_name = BodyParameter('name')
    task_name_like = BodyParameter('nameLike')
    description = BodyParameter('description')
    description_like = BodyParameter('descriptionLike')
    priority = BodyParameter('priority')
    max_priority = BodyParameter('maxPriority')
    min_priority = BodyParameter('minPriority')
    tenant_id_in = BodyParameter('tenantIdIn')
    without_tenant_id = BodyParameter('withoutTenantId')
    created_before = BodyParameter('createdBefore')
    created_after = BodyParameter('createdAfter')
    due_before = BodyParameter('dueBefore')
    due_after = BodyParameter('dueAfter')
    follow_up_after = BodyParameter('followUpAfter')
    follow_up_before = BodyParameter('followUpBefore')
    follow_up_before_or_not_existent = BodyParameter('followUpBeforeOrNotExistent')
    query = BodyParameterContainer(
        'query',
        process_instance_id,
        process_instance_business_key,
        process_instance_business_key_like,
        process_definition_id,
        process_definition_key,
        process_definition_key_in,
        process_definition_name,
        process_definition_name_like,
        case_instance_id,
        case_instance_business_key,
        case_instance_business_key_like,
        case_definition_id,
        case_definition_key,
        case_definition_name,
        case_definition_name_like,
        active,
        activity_instance_id_in,
        execution_id,
        assignee,
        assignee_in,
        assignee_like,
        task_owner,
        candidate_group,
        candidate_groups,
        candidate_user,
        involved_user,
        unassigned,
        delegation_state,
        task_definition_key,
        task_definition_key_in,
        task_definition_key_like,
        task_name,
        task_name_like,
        description,
        description_like,
        priority,
        max_priority,
        min_priority,
        tenant_id_in,
        without_tenant_id,
        created_before,
        created_after,
        due_before,
        due_after,
        follow_up_after,
        follow_up_before,
        follow_up_before_or_not_existent
    )

    def add_process_instance_criteria(
        self,
        id_: str = ...,
        business_key: str = ...,
        business_key_like: str = ...
    ) -> None:
        """Add criteria that filter by process instance.

        :param id_: Filter by the id of the process instance.
        :param business_key: Filter by the business key of the process instance.
        :param business_key_like: Filter by a substring of the business key of the filter.
        """
        if id_ is not Ellipsis:
            self.process_instance_id = id_
        if business_key is not Ellipsis:
            self.process_instance_business_key = business_key
        if business_key_like is not Ellipsis:
            self.process_instance_business_key_like = business_key_like

    def add_process_definition_criteria(
        self,
        id_: str = ...,
        key: str = ...,
        key_in: typing.Iterable[str] = ...,
        name: str = ...,
        name_like: str = ...
    ) -> None:
        """Add criteria that filter by the process definition.

        :param id_: Filter by the id of the process definition.
        :param key: Filter by the key of the process definition.
        :param key_in: Filter by a substring of the key of the process definition.
        :param name: Filter by the name of the process definition.
        :param name_like: Filter by a substring of the name of the process definition.
        """
        if id_ is not Ellipsis:
            self.process_definition_id = id_
        if key is not Ellipsis:
            self.process_definition_key = key
        if key_in is not Ellipsis:
            self.process_definition_key_in = key_in
        if name is not Ellipsis:
            self.process_definition_name = name
        if name_like is not Ellipsis:
            self.process_definition_name_like = name_like

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
            self.case_instance_id = id_
        if business_key is not Ellipsis:
            self.case_instance_business_key = business_key
        if business_key_like is not Ellipsis:
            self.case_instance_business_key_like = business_key_like

        return self

    def add_case_definition_criteria(
        self,
        id_: str = ...,
        key: str = ...,
        name: str = ...,
        name_like: str = ...
    ) -> None:
        """Add criteria that filter by the case definition.

        :param id_: Filter by the id of the case definition.
        :param key: Filter by the key of the case definition.
        :param name: Filter by the name of the case definition.
        :param name_like: Filter by a substring of the name of the case definition.
        """
        if id_ is not Ellipsis:
            self.case_definition_id = id_
        if key is not Ellipsis:
            self.case_definition_key = key
        if name is not Ellipsis:
            self.case_definition_name = name
        if name_like is not Ellipsis:
            self.case_definition_name_like = name_like

    def add_other_criteria(
        self,
        active: bool = ...,
        activity_instance_id_in: typing.Iterable[str] = ...,
        execution_id: str = ...
    ) -> None:
        """Add criteria that filter by active status, activity instance or execution id.

        :param active: Filter only active tasks.
        :param activity_instance_id_in: Filter by activity instance ids.
        :param execution_id: Filter by the execution id.
        """
        if active is not Ellipsis:
            self.active = active or None
        if activity_instance_id_in is not Ellipsis:
            self.activity_instance_id_in = activity_instance_id_in
        if execution_id is not Ellipsis:
            self.execution_id = execution_id

    def add_user_criteria(
        self,
        assignee: str = ...,
        assignee_in: typing.Iterable[str] = ...,
        assignee_like: str = ...,
        task_owner: str = ...,
        candidate_group: str = ...,
        candidate_groups: typing.Iterable[str] = ...,
        candidate_user: str = ...,
        involved_user: str = ...,
        unassigned: bool = ...,
        delegation_state: typing.Union[str, pycamunda.task.DelegationState] = ...
    ) -> None:
        """Add criteria that filter by user.

        :param assignee: Filter by the assignee of the task.
        :param assignee_in: Filter whether assignee of the task is one of multiple ones.
        :param assignee_like: Filter by a substring of the assignee of the task.
        :param task_owner: Filter by the owner of the task.
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
            self.assignee = assignee
        if assignee_in is not Ellipsis:
            self.assignee_in = assignee_in
        if assignee_like is not Ellipsis:
            self.assignee_like = assignee_like
        if task_owner is not Ellipsis:
            self.task_owner = task_owner
        if candidate_group is not Ellipsis:
            self.candidate_group = candidate_group
        if candidate_groups is not Ellipsis:
            self.candidate_groups = candidate_groups
        if candidate_user is not Ellipsis:
            self.candidate_user = candidate_user
        if involved_user is not Ellipsis:
            self.involved_user = involved_user
        if unassigned is not Ellipsis:
            self.unassigned = unassigned
        if delegation_state is not Ellipsis:
            self.delegation_state = None
            if delegation_state is not None:
                self.delegation_state = pycamunda.task.DelegationState(delegation_state)

    def add_task_criteria(
        self,
        definition_key: str = ...,
        definition_key_in: typing.Iterable[str] = ...,
        definition_key_like: str = ...,
        task_name: str = ...,
        task_name_like: str = ...,
        description: str = ...,
        description_like: str = ...,
        priority: int = ...,
        max_priority: int = ...,
        min_priority: int = ...,
        tenant_id_in: typing.Iterable[str] = ...,
        without_tenant_id: bool = False
    ) -> None:
        """Add criteria that filter by task.

        :param definition_key: Filter by the definition key of the task.
        :param definition_key_in: Filter whether definition key of the task is one of multiple ones.
        :param definition_key_like: Filter by a substring of the definition key of the task.
        :param task_name: Filter by the name of the task.
        :param task_name_like:  Filter by a substring of the name of the task.
        :param description: Filter by the description of the task.
        :param description_like: Filter by a substring of the description of the task.
        :param priority: Filter by the priority of the task.
        :param max_priority: Filter by a maximum priority of the task.
        :param min_priority: Filter by a minimum priority of the task.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Filter only tasks without tenant id.
        """
        if definition_key is not Ellipsis:
            self.task_definition_key = definition_key
        if definition_key_in is not Ellipsis:
            self.task_definition_key_in = definition_key_in
        if definition_key_like is not Ellipsis:
            self.task_definition_key_like = definition_key_like
        if task_name is not Ellipsis:
            self.task_name = task_name
        if task_name_like is not Ellipsis:
            self.task_name_like = task_name_like
        if description is not Ellipsis:
            self.description = description
        if description_like is not Ellipsis:
            self.description_like = description_like
        if priority is not Ellipsis:
            self.priority = priority
        if max_priority is not Ellipsis:
            self.max_priority = max_priority
        if min_priority is not Ellipsis:
            self.min_priority = min_priority
        if tenant_id_in is not Ellipsis:
            self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id

    def add_datetime_criteria(
        self,
        created_before: dt.datetime = ...,
        created_after: dt.datetime = ...,
        due_before: dt.datetime = ...,
        due_after: dt.datetime = ...,
        follow_up_after: dt.datetime = ...,
        follow_up_before: dt.datetime = ...,
        follow_up_before_or_not_existent: dt.datetime = ...
    ) -> None:
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
            self.created_before = created_before
        if created_after is not Ellipsis:
            self.created_after = created_after
        if due_before is not Ellipsis:
            self.due_before = due_before
        if due_after is not Ellipsis:
            self.due_after = due_after
        if follow_up_after is not Ellipsis:
            self.follow_up_after = follow_up_after
        if follow_up_before is not Ellipsis:
            self.follow_up_before = follow_up_before
        if follow_up_before_or_not_existent is not Ellipsis:
            self.follow_up_before_or_not_existent = follow_up_before_or_not_existent

    def __call__(self, *args, **kwargs):
        return NotImplementedError


class Create(_Criteria):

    resource_type = BodyParameter('resourceType')
    name = BodyParameter('name')
    owner = BodyParameter('owner')

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

    def __call__(self, *args, **kwargs) -> Filter:
        """Send the request"""
        params = self.body_parameters()
        try:
            response = requests.post(self.url, json=params)
        except requests.exceptions.RequestException as exc:
            raise pycamunda.PyCamundaException(exc)
        if not response:
            pycamunda.base._raise_for_status(response)

        return Filter.load(response.json())


class Update(_Criteria):

    id_ = PathParameter('id')
    resource_type = BodyParameter('resourceType')
    name = BodyParameter('name')
    owner = BodyParameter('owner')

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

    def __call__(self, *args, **kwargs) -> None:
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

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        try:
            response = requests.delete(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)


class Execute(_Criteria):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str, single_result: bool = False):
        """Execute a filter.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the filter.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.single_result = single_result

    def __call__(
        self, *args, **kwargs
    ) -> typing.Union[pycamunda.task.Task, typing.Tuple[pycamunda.task.Task]]:
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

    def __call__(self, *args, **kwargs) -> int:
        """Send the request."""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return response.json()['count']
