# -*- coding: utf-8 -*-

"""This module provides access to the external task REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing

import pycamunda
import pycamunda.base
import pycamunda.variable
import pycamunda.batch
from pycamunda.request import QueryParameter

URL_SUFFIX = '/history/process-instance'


__all__ = [
    'GetList'
]


@dataclasses.dataclass
class HistoryProcessInstance:
    """Data class of HistoryProcessInstance returned by the REST api of Camunda."""
    id_: str
    business_key: str
    process_definition_id: str
    process_definition_key: str
    process_definition_name: str
    process_definition_version: str
    start_time: str
    end_time: str
    removal_time: str
    duration_in_millis: str
    start_user_id: str
    start_activity_id: str
    delete_reason: str
    root_process_instance_id: str
    super_process_instance_id: str
    super_case_instance_id: str
    case_instance_id: str
    tenant_id: str
    state: str

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> HistoryProcessInstance:
        history_process_instance = cls(
            id_=data['id'],
            business_key=data['businessKey'],
            process_definition_id=data['processDefinitionId'],
            process_definition_key=data['processDefinitionKey'],
            process_definition_name=data['processDefinitionName'],
            process_definition_version=data['processDefinitionVersion'],
            start_time=data['startTime'],
            end_time=data['endTime'],
            removal_time=data['removalTime'],
            duration_in_millis=data['durationInMillis'],
            start_user_id=data['startUserId'],
            start_activity_id=data['startActivityId'],
            delete_reason=data['deleteReason'],
            root_process_instance_id=data['rootProcessInstanceId'],
            super_process_instance_id=data['superProcessInstanceId'],
            super_case_instance_id=data['superCaseInstanceId'],
            case_instance_id=data['caseInstanceId'],
            tenant_id=data['tenantId'],
            state=data['state']
        )
        return history_process_instance


class GetList(pycamunda.base.CamundaRequest):
    process_instance_id = QueryParameter('processInstanceId')
    # process_instance_ids = QueryParameter('processInstanceIds')
    process_definition_id = QueryParameter('processDefinitionId')
    process_definition_key = QueryParameter('processDefinitionKey')
    # process_definition_key_in = QueryParameter('processDefinitionKeyIn')
    process_definition_name = QueryParameter('processDefinitionName')
    process_definition_name_like = QueryParameter('processDefinitionNameLike')
    process_definition_key_not_in = QueryParameter('processDefinitionKeyNotIn')
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')
    process_instance_business_key = QueryParameter('processInstanceBusinessKey')
    process_instance_business_key_in = QueryParameter('processInstanceBusinessKeyIn')
    process_instance_business_key_like = QueryParameter('processInstanceBusinessKeyLike')
    root_process_instances = QueryParameter('rootProcessInstances')
    unfinished = QueryParameter('unfinished')
    with_incidents = QueryParameter('withIncidents')
    with_root_incidents = QueryParameter('withRootIncidents')
    incident_type = QueryParameter('incidentType')
    incident_status = QueryParameter('incidentStatus')
    incident_message = QueryParameter('incidentMessage')
    incident_message_like = QueryParameter('incidentMessageLike')
    started_before = QueryParameter('startedBefore')
    started_after = QueryParameter('startedAfter')
    finished_before = QueryParameter('finishedBefore')
    finished_after = QueryParameter('finishedAfter')
    executed_activity_after = QueryParameter('executedActivityAfter')
    executed_activity_before = QueryParameter('executedActivityBefore')
    executed_job_after = QueryParameter('executedJobAfter')
    executed_job_before = QueryParameter('executedJobBefore')
    started_by = QueryParameter('startedBy')
    super_process_instance_id = QueryParameter('superProcessInstanceId')
    sub_process_instance_id = QueryParameter('subProcessInstanceId')
    super_case_instance_id = QueryParameter('superCaseInstanceId')
    sub_case_instance_id = QueryParameter('subCaseInstanceId')
    case_instance_id = QueryParameter('caseInstanceId')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId')
    executed_activity_id_in = QueryParameter('executedActivityIdIn')
    active_activity_id_in = QueryParameter('activeActivityIdIn')
    active = QueryParameter('active')
    suspended = QueryParameter('suspended')
    completed = QueryParameter('completed')
    externally_terminated = QueryParameter('externallyTerminated')
    internally_terminated = QueryParameter('internallyTerminated')
    variables = QueryParameter('variables')
    variable_names_ignore_case = QueryParameter('variableNamesIgnoreCase')
    variable_values_ignore_case = QueryParameter('variableValuesIgnoreCase')
    sort_by = QueryParameter(
        'sortBy',
        mapping={
         'id_': 'id',
         'instance_id': 'instanceId',
         'definition_id': 'definitionId',
         'definition_key': 'definitionKey',
         'definition_name': 'definitionName',
         'definition_version': 'definitionVersion',
         'business_key': 'businessKey',
         'start_time': 'startTime',
         'end_time': 'endTime',
         'duration': 'duration',
         'tenant_id': 'tenanId'
        }
    )
    ascending = QueryParameter(
        'sortOrder',
        mapping={True: 'asc', False: 'desc'},
        provide=lambda self, obj, obj_type: vars(obj).get('sort_by', None) is not None
    )

    def __init__(
        self,
        url: str,
        id_: str = None,
        active: bool = None,
        active_activity_id_in: str = None,
        ascending: bool = None,
        case_instance_id: str = None,
        completed: bool = None,
        executed_activity_after: str = None,
        executed_activity_before: str = None,
        executed_activity_id_in: str = None,
        executed_job_after: str = None,
        executed_job_before: str = None,
        externally_terminated: bool = None,
        finished_after: str = None,
        finished_before: str = None,
        first_result: int = None,
        incident_message: str = None,
        incident_message_like: str = None,
        incident_status: str = None,
        incident_type: str = None,
        internally_terminated: bool = None,
        max_results: int = None,
        process_definition_key: str = None,
        process_instance_business_key: str = None,
        process_instance_business_key_in: str = None,
        process_instance_business_key_like: str = None,
        process_instance_id: str = None,
        root_process_instances: str = None,
        sort_by: str = None,
        started_after: str = None,
        started_before: str = None,
        started_by: str = None,
        sub_case_instance_id: str = None,
        sub_process_instance_id: str = None,
        super_case_instance_id: str = None,
        super_process_instance_id: str = None,
        suspended: bool = None,
        tenant_id_in: str = None,
        unfinished: bool = None,
        variable_names_ignore_case: bool = None,
        variable_values_ignore_case: bool = None,
        variables: str = None,
        with_incidents: bool = None,
        with_root_incidents: str = None,
        without_tenant_id: bool = None
    ):
        """Query for a list of external tasks using a list of parameters. The size of the result set
        can be retrieved by using the Get Count request.

        :param url: Camunda Rest engine URL.
        :param id_: Filter by the id of the external task.
        :param process_instance_id: Filter by the process_instance_id
        """
        super().__init__(url=url + URL_SUFFIX)
        self.id_ = id_
        self.active = active
        self.active_activity_id_in = active_activity_id_in
        self.ascending = ascending
        self.case_instance_id = case_instance_id
        self.completed = completed
        self.executed_activity_after = executed_activity_after
        self.executed_activity_before = executed_activity_before
        self.executed_activity_id_in = executed_activity_id_in
        self.executed_job_after = executed_job_after
        self.executed_job_before = executed_job_before
        self.externally_terminated = externally_terminated
        self.finished_after = finished_after
        self.finished_before = finished_before
        self.first_result = first_result
        self.incident_message = incident_message
        self.incident_message_like = incident_message_like
        self.incident_status = incident_status
        self.incident_type = incident_type
        self.internally_terminated = internally_terminated
        self.max_results = max_results
        self.process_definition_key = process_definition_key
        self.process_instance_business_key = process_instance_business_key
        self.process_instance_business_key_in = process_instance_business_key_in
        self.process_instance_business_key_like = process_instance_business_key_like
        self.process_instance_id = process_instance_id
        self.root_process_instances = root_process_instances
        self.sort_by = sort_by
        self.started_after = started_after
        self.started_before = started_before
        self.started_by = started_by
        self.sub_case_instance_id = sub_case_instance_id
        self.sub_process_instance_id = sub_process_instance_id
        self.super_case_instance_id = super_case_instance_id
        self.super_process_instance_id = super_process_instance_id
        self.suspended = suspended
        self.suspended = suspended
        self.tenant_id_in = tenant_id_in
        self.unfinished = unfinished
        self.variable_names_ignore_case = variable_names_ignore_case
        self.variable_values_ignore_case = variable_values_ignore_case
        self.variables = variables
        self.with_incidents = with_incidents
        self.with_root_incidents = with_root_incidents
        self.without_tenant_id = without_tenant_id

    def __call__(self, *args, **kwargs) -> typing.Tuple[HistoryProcessInstance]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)
        return tuple(HistoryProcessInstance.load(data_json) for data_json in response.json())
