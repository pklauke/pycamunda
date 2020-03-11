# -*- coding: utf-8 -*-

"""This module provides access to the external task REST api of Camunda."""

import dataclasses

import requests

import pycamunda
import pycamunda.request
from pycamunda.request import PathParameter, QueryParameter, BodyParameter, BodyParameterContainer


URL_SUFFIX = '/external-task'


@dataclasses.dataclass
class ExternalTask:
    activity_id: str
    activity_instance_id: str
    error_message: str
    error_details: str
    execution_id: str
    id_: str
    lock_expiration_time: str
    process_definition_id: str
    process_definition_key: str
    process_instance_id: str
    tenant_id: str
    retries: int
    suspended: bool
    worker_id: str
    priority: str
    topic_name: str
    business_key: str

    @classmethod
    def load(cls, data):
        return ExternalTask(
            activity_id=data['activityId'],
            activity_instance_id=data['activityInstanceId'],
            error_message=data['errorMessage'],
            error_details=data['errorDetails'],
            execution_id=data['executionId'],
            id_=data['id'],
            lock_expiration_time=data['lockExpirationTime'],
            process_definition_id=data['processDefinitionId'],
            process_definition_key=data['processDefinitionKey'],
            process_instance_id=data['processInstanceId'],
            tenant_id=data['tenantId'],
            retries=data['retries'],
            suspended=data['suspended'],
            worker_id=data['workerId'],
            priority=data['priority'],
            topic_name=data['topicName'],
            business_key=data['businessKey']
        )


class Get(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url, id_):
        """Query for an external task.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the external task.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def send(self):
        """Send the request"""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return ExternalTask.load(response.json())


class GetList(pycamunda.request.CamundaRequest):

    id_ = QueryParameter('externalTaskId')
    topic_name = QueryParameter('topicName')
    worker_id = QueryParameter('workerId')
    locked = QueryParameter('locked', provide=pycamunda.request.value_is_true)
    not_locked = QueryParameter('notLocked', provide=pycamunda.request.value_is_true)
    with_retries_left = QueryParameter('withRetriesLeft',
                                       provide=pycamunda.request.value_is_true)
    no_retries_left = QueryParameter('noRetriesLeft',
                                     provide=pycamunda.request.value_is_true)
    lock_expiration_after = QueryParameter('lockExpirationAfter')
    lock_expiration_before = QueryParameter('lockExpirationBefore')
    activity_id = QueryParameter('activityId')
    actitity_id_in = QueryParameter('activityIdIn')
    execution_id = QueryParameter('executionId')
    process_instance_id = QueryParameter('processInstanceId')
    process_definition_id = QueryParameter('processDefinitionId')
    tenant_id_in = QueryParameter('tenantIdIn')
    active = QueryParameter('active', provide=pycamunda.request.value_is_true)
    priority_higher_equals = QueryParameter('priorityHigherThanOrEquals')
    priority_lower_equals = QueryParameter('priorityLowerThanOrEquals')
    suspended = QueryParameter('suspended', provide=pycamunda.request.value_is_true)
    sort_by = QueryParameter('sortBy',
                             mapping={
                                 'id_': 'id',
                                 'lock_expiration_time': 'lockExpirationTime',
                                 'process_instance_id': 'processInstanceId',
                                 'process_definition_id': 'processDefinitionId',
                                 'tenant_id': 'tenantId',
                                 'task_priority': 'taskPriority'
                             })
    ascending = QueryParameter('sortOrder', mapping={True: 'asc', False: 'desc'},
                               provide=lambda self, obj, obj_type: 'sort_by' in vars(self))
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')

    def __init__(self, url, id_=None, topic_name=None, worker_id=None, locked=False,
                 not_locked=False, with_retries_left=False, no_retries_left=False,
                 lock_expiration_after=None, lock_expiration_before=None, activity_id=None,
                 activity_id_in=None, execution_id=None, process_instance_id=None,
                 process_definition_id=None, tenant_id_in=None, active=False,
                 priority_higher_equals=None, priority_lower_equals=None, suspended=False,
                 sort_by=None, ascending=True, first_result=None, max_results=None):
        """Query for a list of external tasks using a list of parameters. The size of the result set
        can be retrieved by using the Get Count request.

        :param id_: Filter by the id of the external task.
        :param topic_name: Filter by the topic name of the external task.
        :param worker_id: Filter by the id of the worker the task was locked by last.
        :param locked: Include only locked external tasks.
        :param not_locked: Include only unlocked tasks.
        :param with_retries_left: Include only external tasks that have retries left.
        :param no_retries_left: Include only external tasks that have no retries left.
        :param lock_expiration_after: Include only external tasks with a lock that expires after a
                                      date.
        :param lock_expiration_before: Include only external tasks with a lock that expires before a
                                       date.
        :param activity_id: Filter by activity id the external task is created for.
        :param activity_id_in: Filter whether activity id is one of multiple ones.
        :param execution_id: Filter by the execution id the external task belongs to.
        :param process_instance_id: Filter by the process instance id the external task belongs to.
        :param process_definition_id: Filter by the process definition id the external task belongs
                                      to.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param active: Include only external tasks that are active.
        :param priority_higher_equals: Include only external tasks with a priority higher than or
                                       equals to the given value.
        :param priority_lower_equals: Include only external tasks with a priority lower than or
                                      equals to the given value.
        :param suspended: Include only external tasks that are suspended.
        :param sort_by: Sort the results by `id_`, `lock_expiration_time, `process_instance_id`,
                        `process_definition_key`, `tenant_id` or `task_priority`.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url + URL_SUFFIX)
        self.id_ = id_
        self.topic_name = topic_name
        self.worker_id = worker_id
        self.locked = locked
        self.not_locked = not_locked
        self.with_retries_left = with_retries_left
        self.no_retries_left = no_retries_left
        self.lock_expiration_after = lock_expiration_after
        self.lock_expiration_before = lock_expiration_before
        self.activity_id = activity_id
        self.actitity_id_in = activity_id_in
        self.execution_id = execution_id
        self.process_instance_id = process_instance_id
        self.process_definition_id = process_definition_id
        self.tenant_id_in = tenant_id_in
        self.active = active
        self.priority_higher_equals = priority_higher_equals
        self.priority_lower_equals = priority_lower_equals
        self.suspended = suspended
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

        return tuple(ExternalTask.load(task_json) for task_json in response.json())


class Count(GetList):

    def __init__(self, url, id_=None, topic_name=None, worker_id=None, locked=False,
                 not_locked=False, with_retries_left=False, no_retries_left=False,
                 lock_expiration_after=None, lock_expiration_before=None, activity_id=None,
                 activity_id_in=None, execution_id=None, process_instance_id=None,
                 process_definition_id=None, tenant_id_in=None, active=False,
                 priority_higher_equals=None, priority_lower_equals=None, suspended=False,
                 sort_by=None, ascending=True, first_result=None, max_results=None):
        """Get the size of the result returned by the Get List request.

        :param id_: Filter by the id of the external task.
        :param topic_name: Filter by the topic name of the external task.
        :param worker_id: Filter by the id of the worker the task was locked by last.
        :param locked: Include only locked external tasks.
        :param not_locked: Include only unlocked tasks.
        :param with_retries_left: Include only external tasks that have retries left.
        :param no_retries_left: Include only external tasks that have no retries left.
        :param lock_expiration_after: Include only external tasks with a lock that expires after a
                                      date.
        :param lock_expiration_before: Include only external tasks with a lock that expires before a
                                       date.
        :param activity_id: Filter by activity id the external task is created for.
        :param activity_id_in: Filter whether activity id is one of multiple ones.
        :param execution_id: Filter by the execution id the external task belongs to.
        :param process_instance_id: Filter by the process instance id the external task belongs to.
        :param process_definition_id: Filter by the process definition id the external task belongs
                                      to.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param active: Include only external tasks that are active.
        :param priority_higher_equals: Include only external tasks with a priority higher than or
                                       equals to the given value.
        :param priority_lower_equals: Include only external tasks with a priority lower than or
                                      equals to the given value.
        :param suspended: Include only external tasks that are suspended.
        :param sort_by: Sort the results by `id_`, `lock_expiration_time, `process_instance_id`,
                        `process_definition_key`, `tenant_id` or `task_priority`.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url,
                         id_=id_, topic_name=topic_name, worker_id=worker_id,
                         locked=locked, not_locked=not_locked, with_retries_left=with_retries_left,
                         no_retries_left=no_retries_left,
                         lock_expiration_after=lock_expiration_after,
                         lock_expiration_before=lock_expiration_before, activity_id=activity_id,
                         activity_id_in=activity_id_in, execution_id=execution_id,
                         process_instance_id=process_instance_id,
                         process_definition_id=process_definition_id, tenant_id_in=tenant_id_in,
                         active=active,
                         priority_higher_equals=priority_higher_equals,
                         priority_lower_equals=priority_lower_equals, suspended=suspended,
                         sort_by=sort_by, ascending=ascending, first_result=first_result,
                         max_results=max_results)
        self._url += '/count'

    def send(self):
        """Send the request"""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return int(response.json()['count'])
