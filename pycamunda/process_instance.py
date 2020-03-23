# -*- coding: utf-8 -*-

"""This module provides access to the process instance REST api of Camunda."""

from __future__ import annotations
import dataclasses
import numbers
import typing

import requests

import pycamunda.variable
import pycamunda.request
import pycamunda.activity_instance
from pycamunda.request import PathParameter, QueryParameter, BodyParameter, BodyParameterContainer


URL_SUFFIX = '/process-instance'


@dataclasses.dataclass
class ProcessInstance:
    id_: str
    definition_id: str
    business_key: str
    case_instance_id: str
    tenant_id: str
    ended: bool
    suspended: bool
    links: typing.Tuple[pycamunda.Link]
    variables: typing.Dict[str, pycamunda.variable.Variable] = None

    @classmethod
    def load(cls, data) -> ProcessInstance:
        process_instance = cls(
            id_=data['id'],
            definition_id=data['definitionId'],
            business_key=data['businessKey'],
            case_instance_id=data['caseInstanceId'],
            tenant_id=data['tenantId'],
            ended=data['ended'],
            suspended=data['suspended'],
            links=tuple(pycamunda.Link.load(link_json) for link_json in data['links']),
        )
        try:
            variables = data['variables']
        except KeyError:
            pass
        else:
            process_instance.variables = {name: pycamunda.variable.Variable.load(var_json)
                                          for name, var_json in variables.items()}

        return process_instance


class Delete(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')
    skip_custom_listeners = QueryParameter('skipCustomListeners')
    skip_io_mappings = QueryParameter('skipIoMappings')
    skip_subprocesses = QueryParameter('skipSubprocesses')
    fail_if_not_exists = QueryParameter('failIfNotExists')

    def __init__(
            self,
            url: str,
            id_: str,
            skip_custom_listeners: bool = False,
            skip_io_mappings: bool = False,
            skip_subprocesses: bool = False,
            fail_if_not_exists: bool = True
    ):
        """Delete a process instance.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process instance.
        :param skip_custom_listeners: Whether to skip custom listeners and notify only builtin ones.
        :param skip_io_mappings: Whether to skip input/output mappings.
        :param skip_subprocesses: Whether to skip subprocesses.
        :param fail_if_not_exists: Whether to fail if the provided process instance id is not found.
        """
        super().__init__(url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.skip_custom_listeners = skip_custom_listeners
        self.skip_io_mappings = skip_io_mappings
        self.skip_subprocesses = skip_subprocesses
        self.fail_if_not_exists = fail_if_not_exists

    def send(self):
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.delete(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)


class GetActivityInstance(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get an activity instance tree for a specific process instance.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process instance.
        """
        super().__init__(url + URL_SUFFIX + '/{id}/activity-instances')
        self.id_ = id_

    def send(self) -> pycamunda.activity_instance.ActivityInstance:
        """Send the request."""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return pycamunda.activity_instance.ActivityInstance.load(response.json())


class GetList(pycamunda.request.CamundaRequest):

    process_instance_ids = QueryParameter('processInstanceIds')
    business_key = QueryParameter('businessKey')
    business_key_like = QueryParameter('businessKeyLike')
    case_instance_id = QueryParameter('caseInstanceId')
    process_definition_id = QueryParameter('processDefinitionId')
    process_definition_key = QueryParameter('processDefinitionKey')
    process_definition_key_in = QueryParameter('processDefinitionKeyIn')
    process_definition_key_not_in = QueryParameter('processDefinitionKeyNotIn')
    deployment_id = QueryParameter('deploymentId')
    super_process_instance_id = QueryParameter('superProcessInstance')
    sub_process_instance_id = QueryParameter('subProcessInstance')
    super_case_instance_id = QueryParameter('superCaseInstance')
    sub_case_instance_id = QueryParameter('subCaseInstance')
    active = QueryParameter('active', provide=pycamunda.request.value_is_true)
    suspended = QueryParameter('suspended', provide=pycamunda.request.value_is_true)
    with_incident = QueryParameter('withIncident')
    incident_id = QueryParameter('incidentId')
    incident_type = QueryParameter('incidentType')
    incident_message = QueryParameter('incidentMessage')
    incident_message_like = QueryParameter('incidentMessageLike')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.request.value_is_true)
    activity_id_in = QueryParameter('activityIdIn')
    root_process_instances = QueryParameter('rootProcessInstances')
    leaf_process_instances = QueryParameter('leafProcessInstances')
    process_definition_without_tenant_id_in = QueryParameter('processDefinitionWithoutTenantIdIn')
    variables = QueryParameter('variables')
    variable_names_ignore_case = QueryParameter('variableNamesIgnoreCase')
    variable_values_ignore_case = QueryParameter('variableValuesIgnoreCase')
    sort_by = QueryParameter(
        'sortBy',
        mapping={'instance_id': 'instanceId', 'definition_key': 'definitionKey',
                 'definition_id': 'definitionId', 'tenant_id': 'tenantId',
                 'business_key': 'businessKey'}
    )
    ascending = QueryParameter('sortOrder', mapping={True: 'asc', False: 'desc'},
                               provide=lambda self, obj, obj_type: 'sort_by' in vars(self))
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')

    def __init__(
            self,
            url: str,
            process_instance_ids: typing.Iterable[str] = None,
            business_key: str = None,
            business_key_like: str = None,
            case_instance_id: str = None,
            process_definition_id: str = None,
            process_definition_key: str = None,
            process_definition_key_in: typing.Iterable[str] = None,
            process_definition_key_not_in: typing.Iterable[str] = None,
            deployment_id: str = None,
            super_process_instance_id: str = None,
            sub_process_instance_id: str = None,
            super_case_instance_id: str = None,
            sub_case_instance_id: str = None,
            active: bool = False,
            suspended: bool = False,
            with_incident: bool = None,
            incident_id: str = None,
            incident_type: str = None,  # TODO allow inputting IncidentType
            incident_message: str = None,
            incident_message_like: str = None,
            tenant_id_in: typing.Iterable[str] = None,
            without_tenant_id: bool = False,
            activity_id_in: typing.Iterable[str] = None,
            root_process_instances: bool = None,
            leaf_process_instances: bool = None,
            process_definition_without_tenant_id: bool = None,
            variables = None,  # TODO add annotation
            variable_names_ignore_case: bool = None,
            variable_values_ignore_case: bool = None,
            sort_by: str = None,
            ascending: bool = True,
            first_result: numbers.Integral = None,
            max_results: numbers.Integral = None
    ):
        """Get a list of process instances.

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
        :param super_process_instance_id: Filter process instances that are a sub process of the
                                          provided id.
        :param sub_process_instance_id: Filter process instances that are a super process of the
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
        :param process_definition_without_tenant_id: Include only process instance where the
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
        super().__init__(url + URL_SUFFIX)
        self.process_instance_ids = process_instance_ids
        self.business_key = business_key
        self.business_key_like = business_key_like
        self.case_instance_id = case_instance_id
        self.process_definition_id = process_definition_id
        self.process_definition_key = process_definition_key
        self.process_definition_key_in = process_definition_key_in
        self.process_definition_key_not_in = process_definition_key_not_in
        self.deployment_id = deployment_id
        self.super_process_instance_id = super_process_instance_id
        self.sub_process_instance_id = sub_process_instance_id
        self.super_case_instance_id = super_case_instance_id
        self.sub_case_instance_id = sub_case_instance_id
        self.active = active
        self.suspended = suspended
        self.with_incident = with_incident
        self.incident_id = incident_id
        self.incident_type = incident_type
        self.incident_message = incident_message
        self.incident_message_like = incident_message_like
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.activity_id_in = activity_id_in
        self.root_process_instances = root_process_instances
        self.leaf_process_instances = leaf_process_instances
        self.process_definition_without_tenant_id_in = process_definition_without_tenant_id
        self.variables = variables
        self.variable_names_ignore_case = variable_names_ignore_case
        self.variable_values_ignore_case = variable_values_ignore_case
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results

    def send(self) -> typing.Tuple[ProcessInstance]:
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return tuple(ProcessInstance.load(instance_json) for instance_json in response.json())


class Get(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get a process instance.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process instance.
        """
        super().__init__(url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def send(self) -> ProcessInstance:
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return ProcessInstance.load(response.json())