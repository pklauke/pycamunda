# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_process_instances_json():
    return [{
        'id': 'anId',
        'definitionId': 'anDefinitionId',
        'businessKey': 'aBusinessKey',
        'caseInstanceId': 'aCaseInstanceId',
        'suspended': False,
        'tenantId': 'aTenantId',
        'links': []
    }]


@pytest.fixture
def evaluate_input():
    return {
        'business_key': 'aKey',
        'tenant_id': 'aTenantId',
        'without_tenant_id': True,
        'process_definition_id': 'anId'
    }


@pytest.fixture
def evaluate_output():
    return {
        'businessKey': 'aKey',
        'tenantId': 'aTenantId',
        'withoutTenantId': True,
        'processDefinitionId': 'anId',
        'variables': {}
    }
