# -*- coding: utf-8 -*-

import pytest


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
def my_execution_json():
    return {
        'id': 'anId',
        'processInstanceId': 'aProcessInstanceId',
        'ended': False,
        'tenantId': 'aTenantId'
    }


@pytest.fixture
def correlate_input():
    return {
        'business_key': 'aKey',
        'process_instance_id': 'anId',
        'tenant_id': 'aTenantId',
        'without_tenant_id': True,
        'result_enabled': True,
        'variables_in_result_enabled': True
    }


@pytest.fixture
def correlate_output():
    return {
        'businessKey': 'aKey',
        'processInstanceId': 'anId',
        'tenantId': 'aTenantId',
        'withoutTenantId': True,
        'resultEnabled': True,
        'variablesInResultEnabled': True,
        'correlationKeys': {},
        'localCorrelationKeys': {},
        'processVariables': {},
        'processVariablesLocal': {}
    }
