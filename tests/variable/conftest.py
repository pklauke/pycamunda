# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_variableinstance_json():
    return {
        'id': 'anId',
        'name': 'aName',
        'type': 'String',
        'value': 'aVal',
        'valueInfo': {},
        'processInstanceId': 'anInstanceId',
        'executionId': 'anExecutionId',
        'caseInstanceId': 'aCaseInstanceId',
        'caseExecutionId': 'anotherExecutionId',
        'taskId': 'aTaskId',
        'activityInstanceId': 'anotherInstanceId',
        'tenantId': 'aTenantId',
        'errorMessage': 'anErrorMessage'
    }


@pytest.fixture
def getlist_input():
    return {
        'name': 'aName',
        'name_like': 'aNam',
        'process_instance_id_in': [],
        'case_instance_id_in': [],
        'case_execution_id_in': [],
        'task_id_in': [],
        'activity_instance_id_in': [],
        'tenant_id_in': [],
        'sort_by': 'name',
        'ascending': False,
        'first_result': 1,
        'max_results': 10,
        'deserialize_values': True
    }


@pytest.fixture
def getlist_output():
    return {
        'variableName': 'aName',
        'variableNameLike': 'aNam',
        'processInstanceIdIn': [],
        'caseInstanceIdIn': [],
        'caseExecutionIdIn': [],
        'taskIdIn': [],
        'activityInstanceIdIn': [],
        'tenantIdIn': [],
        'sortBy': 'variableName',
        'sortOrder': 'desc',
        'firstResult': 1,
        'maxResults': 10,
        'deserializeValues': 'true'
    }
