# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_case_instance_json():
    return {
        'id': 'anId',
        'caseDefinitionId': 'aDefinitionId',
        'tenantId': 'aTenantId',
        'businessKey': 'aBusinessKey',
        'active': True
    }


@pytest.fixture
def getlist_input():
    return {
        'case_instance_id': 'anId',
        'business_key': 'aKey',
        'case_definition_id': 'anotherId',
        'case_definition_key': 'anotherKey',
        'deployment_id': 'aDeploymentId',
        'super_process_instance': 'aSuperInstanceId',
        'sub_process_instance': 'aSubInstanceId',
        'super_case_instance': 'aSuperCaseInstanceId',
        'sub_case_instance': 'aSubCaseInstanceId',
        'active': True,
        'completed': True,
        'tenant_id_in': [1, 2],
        'without_tenant_id': True,
        'variable_names_ignore_case': True,
        'variable_values_ignore_case': True,
        'sort_by': 'case_instance_id',
        'ascending': False,
        'first_result': 1,
        'max_results': 10
    }


@pytest.fixture
def getlist_output():
    return {
        'caseInstanceId': 'anId',
        'businessKey': 'aKey',
        'caseDefinitionId': 'anotherId',
        'caseDefinitionKey': 'anotherKey',
        'deploymentId': 'aDeploymentId',
        'superProcessInstance': 'aSuperInstanceId',
        'subProcessInstance': 'aSubInstanceId',
        'superCaseInstance': 'aSuperCaseInstanceId',
        'subCaseInstance': 'aSubCaseInstanceId',
        'active': 'true',
        'completed': 'true',
        'tenantIdIn': [1, 2],
        'withoutTenantId': 'true',
        'variables': {},
        'variableNamesIgnoreCase': 'true',
        'variableValuesIgnoreCase': 'true',
        'sortBy': 'caseInstanceId',
        'sortOrder': 'desc',
        'firstResult': 1,
        'maxResults': 10
    }
