# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_incident_json():
    return {
        'id': 'anId',
        'processDefinitionId': 'aDefinitionId',
        'processInstanceId': 'anInstanceId',
        'executionId': 'anExecutionId',
        'incidentType': 'failedExternalTask',
        'activityId': 'anActivityId',
        'causeIncidentId': 'anIncidentId',
        'rootCauseIncidentId': 'anotherIncidentId',
        'configuration': 'aConfiguration',
        'tenantId': 'aTenantId',
        'incidentMessage': 'anIncidentMessage',
        'jobDefinitionId': 'aDefinitionId',
        'incidentTimestamp': '2000-01-01T00:00:00.000+0000'
    }


@pytest.fixture
def getlist_input():
    return {
        'incident_id': 'anId',
        'incident_type': 'failedJob',
        'incident_message': 'anIncidentMessage',
        'process_definition_id': 'aDefinitionId',
        'process_definition_key_in': [],
        'process_instance_id': 'anInstanceId',
        'execution_id': 'anExecutionId',
        'activity_id': 'anActivityId',
        'cause_incident_id': 'anIncidentId',
        'root_cause_incident_id': 'anotherIncidentId',
        'configuration': 'aConfiguration',
        'tenant_id_in': [],
        'job_definition_id_in': [],
        'sort_by': 'incident_id',
        'ascending': False
    }


@pytest.fixture
def getlist_output():
    return {
        'incidentId': 'anId',
        'incidentType': 'failedJob',
        'incidentMessage': 'anIncidentMessage',
        'processDefinitionId': 'aDefinitionId',
        'processDefinitionKeyIn': [],
        'processInstanceId': 'anInstanceId',
        'executionId': 'anExecutionId',
        'activityId': 'anActivityId',
        'causeIncidentId': 'anIncidentId',
        'rootCauseIncidentId': 'anotherIncidentId',
        'configuration': 'aConfiguration',
        'tenantIdIn': [],
        'jobDefinitionIdIn': [],
        'sortBy': 'incidentId',
        'sortOrder': 'desc'
    }
