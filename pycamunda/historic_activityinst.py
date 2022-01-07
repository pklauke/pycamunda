# -*- coding: utf-8 -*-

"""
This module provides activity instance data classes as returned by the REST api of Camunda.
[api-source] https://docs.camunda.org/manual/7.16/reference/rest/history/activity-instance/
"""

from __future__ import annotations
import dataclasses
import typing

import pycamunda.base
from pycamunda.request import QueryParameter, PathParameter, BodyParameter

__all__ = []

Number = typing.TypeVar('Number', int, float)

URL_SUFFIX = "/activity-instance"
URL_PREFIX = "/history"


@dataclasses.dataclass
class HistoricActivityInstance:
    id_: str
    parent_activity_instance_id: str
    activity_id: str
    activity_name: str
    activity_type: str
    process_definition_key: str
    process_definition_id: str
    process_instance_id: str
    execution_id: str
    task_id: str
    assignee: str
    called_process_instance_id: str
    called_case_instance_id: str
    start_time: str
    end_time: str
    duration_in_millis: Number
    canceled: bool
    complete_scope: bool
    tenant_id: str
    removal_time: str
    root_process_instance_id: str

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> HistoricActivityInstance:
        return cls(
            id_=data['id'],
            parent_activity_instance_id=data['parentActivityInstanceId'],
            activity_id=data['activityId'],
            activity_name=data['activityName'],
            activity_type=data['activityType'],
            process_definition_key=data['processDefinitionKey'],
            process_definition_id=data['processDefinitionId'],
            process_instance_id=data['processInstanceId'],
            execution_id=data['executionId'],
            task_id=data['taskId'],
            assignee=data['assignee'],
            called_process_instance_id=data['calledProcessInstanceId'],
            called_case_instance_id=data['calledCaseInstanceId'],
            start_time=data['startTime'],
            end_time=data['endTime'],
            duration_in_millis=data['durationInMillis'],
            canceled=data['canceled'],
            complete_scope=data['completeScope'],
            tenant_id=data['tenantId'],
            removal_time=data['removalTime'],
            root_process_instance_id=data['rootProcessInstanceId']
        )


class Get(pycamunda.base.CamundaRequest):
    pass


class GetList(pycamunda.base.CamundaRequest):
    activity_instance_id = QueryParameter("activityInstanceId")
    process_instance_id = QueryParameter("processInstanceId")
    process_definition_id = QueryParameter("processDefinitionId")
    execution_id = QueryParameter("executionId")
    activity_id = QueryParameter("activityId")
    activity_name = QueryParameter("activityName")
    activity_name_like = QueryParameter("activityNameLike")
    activity_type = QueryParameter("activityType")
    task_assignee = QueryParameter("taskAssignee")
    finished = QueryParameter("finished", provide=pycamunda.base.value_is_true)
    unfinished = QueryParameter("unfinished", provide=pycamunda.base.value_is_true)
    canceled = QueryParameter("canceled")
    complete_scope = QueryParameter("completeScope")
    started_before = QueryParameter("startedBefore")
    started_after = QueryParameter("startedAfter")
    finished_before = QueryParameter("finishedBefore")
    finished_after = QueryParameter("finishedAfter")
    tenant_id_in = QueryParameter("tenantIdIn")
    without_tenant_id = QueryParameter("withoutTenantId", provide=pycamunda.base.value_is_true)
    sort_by = QueryParameter(
        'sortBy',
        mapping={
            'instance_id': 'instanceId',
            'definition_key': 'definitionKey',
            'definition_id': 'definitionId',
            'tenant_id': 'tenantId',
            'business_key': 'businessKey'
        }
    )
    ascending = QueryParameter(
        'sortOrder',
        mapping={True: 'asc', False: 'desc'},
        provide=lambda self, obj, obj_type: vars(obj).get('sort_by', None) is not None
    )
    first_result = QueryParameter("firstResult")
    max_results = QueryParameter("maxResults")

    def __init__(
            self,
            url: str,
            activity_instance_id: str = None,
            process_instance_id: str = None,
            process_definition_id: str = None,
            execution_id: str = None,
            activity_id: str = None,
            activity_name: str = None,
            activity_name_like: str = None,
            activity_type: str = None,
            task_assignee: str = None,
            finished: bool = None,
            unfinished: bool = None,
            canceled: bool = None,
            complete_scope: bool = None,
            started_before: str = None,
            started_after: str = None,
            finished_before: str = None,
            finished_after: str = None,
            tenant_id_in: typing.Iterable[str] = None,
            without_tenant_id: bool = None,
            sort_by: str = None,
            ascending: bool = None,
            first_result: int = None,
            max_results: int = None,
    ):
        """Get a list of historic activities instances.
        # TODO : Fix documenration
        :param url: Camunda Rest engine URL.
        :param process_instance_ids: Filter by process instance ids.
        :param business_key: Filter by business key.
        :param business_key_like: Filter by a substring of the business key.
        :param case_instance_id: Filter by case instance id.
        :param process_definition_id: Filter by process definition id.
        :param process_definition_key: Filter by process definition key.
        :param process_definition_key_in: Filter whether the process definition key is one of
                                          multiple ones.
        :param process_definition_key_not_in: Filter whether the process definition key is not one
                                              of multiple ones.
        :param deployment_id: Filter by deployment id.
        :param super_process_instance: Filter process instances that are a sub process of the
                                          provided id.
        :param sub_process_instance: Filter process instances that are a super process of the
                                        provided id.
        :param super_case_instance_id: Filter process instances that are a sub process of the
                                       provided case instance id.
        :param sub_case_instance_id: Filter process instances that are a super process of the
                                     provided case instance id.
        :param active: Whether to include only active process instances.
        :param suspended: Whether to include only suspended process instances.
        :param with_incident: Whether to include only process instances that have incidents.
        :param incident_id: Filter by incident id.
        :param incident_type: Filter by incident type.
        :param incident_message: Filter by the incident message.
        :param incident_message_like: Filter by a substring the incident message.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Whether to include only process instances that belong to no
                                  tenant.
        :param activity_id_in: Filter whether the activity id is one of multiple ones.
        :param root_process_instances: Include only top level process instances.
        :param leaf_process_instances: Include only bottom level process instances.
        :param process_definition_without_tenant_id_in: Include only process instance where the
                                                     process definition has no tenant id.
        :param variables: # TODO (add via its own method?)
        :param variable_names_ignore_case: Whether to ignore case sensitivity for variables names.
        :param variable_values_ignore_case: Whether to ignore case sensitivity for variable values.
        :param sort_by: Sort the results by 'instance_id', 'definition_key', 'definition_id',
                        'tenant_id', 'business_key'.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url=url + URL_PREFIX + URL_SUFFIX)
        self.activity_instance_id = activity_instance_id
        self.process_instance_id = process_instance_id
        self.process_definition_id = process_definition_id,
        self.execution_id = execution_id,
        self.activity_id = activity_id,
        self.activity_name = activity_name,
        self.activity_name_like = activity_name_like,
        self.activity_type = activity_type,
        self.task_assignee = task_assignee,
        self.finished = finished,
        self.unfinished = unfinished,
        self.canceled = canceled,
        self.complete_scope = complete_scope,
        self.started_before = started_before
        self.started_after = started_after
        self.finished_before = finished_before
        self.finished_after = finished_after
        self.tenant_id_in = tenant_id_in,
        self.without_tenant_id = without_tenant_id,
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results

    def __call__(self, *args, **kwargs) -> typing.Tuple[HistoricActivityInstance]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return tuple(HistoricActivityInstance.load(instance_json) for instance_json in response.json())


class GetListCount(pycamunda.base.CamundaRequest):
    pass
