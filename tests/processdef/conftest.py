# -*- coding: utf-8 -*-

import pytest

import pycamunda.incident


@pytest.fixture
def my_process_definition_json():
    return {
        'id': 'anId',
        'key': 'anKey',
        'category': 'aCategory',
        'description': 'description',
        'name': 'aName',
        'version': 1,
        'resource': 'aResource',
        'deploymentId': 'aDeploymentId',
        'diagram': 'aDiagram',
        'suspended': False,
        'tenantId': 'aTenantId',
        'versionTag': 'aVersionTag',
        'historyTimeToLive': 10,
        'startableInTasklist': True
    }


@pytest.fixture
def my_activity_stats_json():
    return {
        'id': 'anId',
        'instances': 2,
        'failedJobs': 1,
        'incidents': ()
    }


@pytest.fixture
def my_process_instance_stats_json():
    return {
        'id': 'anId',
        'instances': 2,
        'failedJobs': 1,
        'definition': {
            'id': 'anId',
            'key': 'anKey',
            'category': 'aCategory',
            'description': 'description',
            'name': 'aName',
            'version': 1,
            'resource': 'aResource',
            'deploymentId': 'aDeploymentId',
            'diagram': 'aDiagram',
            'suspended': False,
            'tenantId': 'aTenantId',
            'versionTag': 'aVersionTag',
            'historyTimeToLive': 10,
            'startableInTasklist': True
        },
        'incidents': ()
    }


@pytest.fixture
def count_input():
    return {
        'id_': 'anId',
        'id_in': [1],
        'name': 'aName',
        'name_like': 'aNam',
        'deployment_id': 'aDeploymentId',
        'key': 'aKey',
        'key_like': 'aKe',
        'category': 'aCategory',
        'category_like': 'aCategor',
        'version': 1,
        'latest_version': True,
        'resource_name': 'aResourceName',
        'startable_by': 'aStartableBy',
        'active': True,
        'suspended': True,
        'incident_id': 'anIncidentId',
        'incident_type': pycamunda.incident.IncidentType.failed_external_task,
        'incident_message': 'anIncidentMessage',
        'incident_message_like': 'anIncidentMessag',
        'tenant_id_in': [1, 2],
        'without_tenant_id': True,
        'include_without_tenant_id': True,
        'version_tag': 'aVersionTag',
        'version_tag_like': 'aVersionTa',
        'without_version_tag': True,
        'startable_in_tasklist': True,
        'startable_permission_check': True,
        'not_startable_in_tasklist': True,
    }


@pytest.fixture
def count_output():
    return {
        'processDefinitionId': 'anId',
        'processDefinitionIdIn': [1],
        'name': 'aName',
        'nameLike': 'aNam',
        'deploymentId': 'aDeploymentId',
        'key': 'aKey',
        'keyLike': 'aKe',
        'category': 'aCategory',
        'categoryLike': 'aCategor',
        'version': 1,
        'latestVersion': True,
        'resourceName': 'aResourceName',
        'startableBy': 'aStartableBy',
        'active': True,
        'suspended': True,
        'incidentId': 'anIncidentId',
        'incidentType': pycamunda.incident.IncidentType.failed_external_task.value,
        'incidentMessage': 'anIncidentMessage',
        'incidentMessageLike': 'anIncidentMessag',
        'tenantIdIn': [1, 2],
        'withoutTenantId': True,
        'includeProcessDefinitionsWithoutTenantId': True,
        'versionTag': 'aVersionTag',
        'versionTagLike': 'aVersionTa',
        'withoutVersionTag': True,
        'startableInTasklist': True,
        'startablePermissionCheck': 'true',
        'notStartableInTasklist': True,
    }


@pytest.fixture
def getlist_input():
    return {
        'id_': 'anId',
        'id_in': [1],
        'name': 'aName',
        'name_like': 'aNam',
        'deployment_id': 'aDeploymentId',
        'key': 'aKey',
        'key_like': 'aKe',
        'category': 'aCategory',
        'category_like': 'aCategor',
        'version': 1,
        'latest_version': True,
        'resource_name': 'aResourceName',
        'startable_by': 'aStartableBy',
        'active': True,
        'suspended': True,
        'incident_id': 'anIncidentId',
        'incident_type': pycamunda.incident.IncidentType.failed_external_task,
        'incident_message': 'anIncidentMessage',
        'incident_message_like': 'anIncidentMessag',
        'tenant_id_in': [1, 2],
        'without_tenant_id': True,
        'include_without_tenant_id': True,
        'version_tag': 'aVersionTag',
        'version_tag_like': 'aVersionTa',
        'without_version_tag': True,
        'startable_in_tasklist': True,
        'startable_permission_check': True,
        'not_startable_in_tasklist': True,
        'sort_by': 'category',
        'ascending': False,
        'first_result': 1,
        'max_results': 10
    }


@pytest.fixture
def getlist_output():
    return {
        'processDefinitionId': 'anId',
        'processDefinitionIdIn': [1],
        'name': 'aName',
        'nameLike': 'aNam',
        'deploymentId': 'aDeploymentId',
        'key': 'aKey',
        'keyLike': 'aKe',
        'category': 'aCategory',
        'categoryLike': 'aCategor',
        'version': 1,
        'latestVersion': True,
        'resourceName': 'aResourceName',
        'startableBy': 'aStartableBy',
        'active': True,
        'suspended': True,
        'incidentId': 'anIncidentId',
        'incidentType': pycamunda.incident.IncidentType.failed_external_task.value,
        'incidentMessage': 'anIncidentMessage',
        'incidentMessageLike': 'anIncidentMessag',
        'tenantIdIn': [1, 2],
        'withoutTenantId': True,
        'includeProcessDefinitionsWithoutTenantId': True,
        'versionTag': 'aVersionTag',
        'versionTagLike': 'aVersionTa',
        'withoutVersionTag': True,
        'startableInTasklist': True,
        'startablePermissionCheck': 'true',
        'notStartableInTasklist': True,
        'sortBy': 'category',
        'sortOrder': 'desc',
        'firstResult': 1,
        'maxResults': 10
    }


@pytest.fixture
def restartprocessinstance_input():
    return {
        'id_': 'anId',
        'process_instance_ids': [],
        'async_': False,
        'skip_custom_listeners': True,
        'skip_io_mappings': True,
        'initial_variables': True,
        'without_business_key': True
    }


@pytest.fixture
def restartprocessinstance_output():
    return {
        'processInstanceIds': [],
        'skipCustomListeners': True,
        'skipIoMappings': True,
        'initialVariables': True,
        'withoutBusinessKey': True,
        'historicProcessInstanceQuery': {}
    }
