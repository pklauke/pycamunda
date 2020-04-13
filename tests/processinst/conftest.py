# -*- coding: utf-8 -*-

import pytest

import pycamunda.incident


@pytest.fixture
def my_process_instance_json():
    return {
        'id': 'anId',
        'definitionId': 'anDefinitionId',
        'businessKey': 'aBusinessKey',
        'caseInstanceId': 'aCaseInstanceId',
        'suspended': False,
        'tenantId': 'aTenantId',
        'links': []
    }


@pytest.fixture
def delete_input():
    return {
        'id_': 'anId',
        'skip_custom_listeners': False,
        'skip_io_mappings': False,
        'skip_subprocesses': False,
        'fail_if_not_exists': False
    }


@pytest.fixture
def delete_output():
    return {
        'skipCustomListeners': False,
        'skipIoMappings': False,
        'skipSubprocesses': False,
        'failIfNotExists': False
    }


@pytest.fixture
def getlist_input():
    return {
        'process_instance_ids': [],
        'business_key': 'anBusinessKey',
        'business_key_like': 'anotherBusinessKey',
        'case_instance_id': 'anCaseInstanceId',
        'process_definition_id': 'anProcessDefinitionId',
        'process_definition_key': 'anProcessDefinitionKey',
        'process_definition_key_in': [],
        'process_definition_key_not_in': [],
        'deployment_id': 'anDeploymentId',
        'super_process_instance': 'anSuperProcessInstance',
        'sub_process_instance': 'anSubProcessInstance',
        'active': True,
        'suspended': True,
        'with_incident': True,
        'incident_id': 'anIncidentId',
        'incident_type': 'failedExternalTask',
        'incident_message': 'anIncidentMessage',
        'incident_message_like': 'anIncidentMessageLike',
        'tenant_id_in': [],
        'without_tenant_id': True,
        'activity_id_in': [],
        'root_process_instances': True,
        'leaf_process_instances': True,
        'process_definition_without_tenant_id_in': True,
        #'variables': None,  TODO
        'variable_names_ignore_case': True,
        'variable_values_ignore_case': True,
        'sort_by': 'instance_id',
        'ascending': True,
        'first_result': 1,
        'max_results': 10
    }


@pytest.fixture
def getlist_output():
    return {
        'processInstanceIds': [],
        'businessKey': 'anBusinessKey',
        'businessKeyLike': 'anotherBusinessKey',
        'caseInstanceId': 'anCaseInstanceId',
        'processDefinitionId': 'anProcessDefinitionId',
        'processDefinitionKey': 'anProcessDefinitionKey',
        'processDefinitionKeyIn': [],
        'processDefinitionKeyNotIn': [],
        'deploymentId': 'anDeploymentId',
        'superProcessInstance': 'anSuperProcessInstance',
        'subProcessInstance': 'anSubProcessInstance',
        'active': True,
        'suspended': True,
        'withIncident': True,
        'incidentId': 'anIncidentId',
        'incidentType': 'failedExternalTask',
        'incidentMessage': 'anIncidentMessage',
        'incidentMessageLike': 'anIncidentMessageLike',
        'tenantIdIn': [],
        'withoutTenantId': True,
        'activityIdIn': [],
        'rootProcessInstances': True,
        'leafProcessInstances': True,
        'processDefinitionWithoutTenantIdIn': True,
        #'variables': None,  TODO
        'variableNamesIgnoreCase': True,
        'variableValuesIgnoreCase': True,
        'sortBy': 'instanceId',
        'sortOrder': 'asc',
        'firstResult': 1,
        'maxResults': 10
    }

