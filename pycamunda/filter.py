# -*- coding: utf-8 -*-

"""This module provides access to the filter REST api of Camunda."""

import requests
import dataclasses

import pycamunda
import pycamunda.request
from pycamunda.request import PathParameter, QueryParameter, BodyParameter, BodyParameterContainer
import pycamunda.task
import pycamunda.variable

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
    sort_by = QueryParameter('sortBy',
                             mapping={'id_': 'filterId', 'first_name': 'firstName',
                                      'last_name': 'lastName', 'email': 'email'})
    ascending = QueryParameter('sortOrder', mapping={True: 'asc', False: 'desc'},
                               provide=lambda self, obj, obj_type: 'sort_by' in vars(self))
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')

    def __init__(self, url, id_=None, name=None, name_like=None, owner=None,
                 item_count=False, sort_by=None, ascending=True, first_result=None,
                 max_results=None):
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
        :param assignee_in: Filter whether assignee of the task is one of multiple ones.
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

    def add_task_criteria(self, definition_key=..., definition_key_in=..., definition_key_like=...,
                          name=..., name_like=..., description=..., description_like=...,
                          priority=..., max_priority=..., min_priority=..., tenant_id_in=...,
                          without_tenant_id=False):
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

    def add_datetime_criteria(self, created_before=..., created_after=..., due_before=...,
                              due_after=..., follow_up_after=..., follow_up_before=...,
                              follow_up_before_or_not_existent=...):
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
            self.query.parameters['createdBefore'] = pycamunda.variable.isoformat(created_before)
        if created_after is not Ellipsis:
            self.query.parameters['createdAfter'] = pycamunda.variable.isoformat(created_after)
        if due_before is not Ellipsis:
            self.query.parameters['dueBefore'] = pycamunda.variable.isoformat(due_before)
        if due_after is not Ellipsis:
            self.query.parameters['dueAfter'] = pycamunda.variable.isoformat(due_after)
        if follow_up_after is not Ellipsis:
            self.query.parameters['followUpAfter'] = pycamunda.variable.isoformat(follow_up_after)
        if follow_up_before is not Ellipsis:
            self.query.parameters['followUpBefore'] = pycamunda.variable.isoformat(follow_up_before)
        if follow_up_before_or_not_existent is not Ellipsis:
            self.query.parameters['followUpBeforeOrNotExistent'] = pycamunda.variable.isoformat(
                follow_up_before_or_not_existent)

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


class Update(pycamunda.request.CamundaRequest, CriteriaMixin):

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


class Execute(pycamunda.request.CamundaRequest, CriteriaMixin):

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
