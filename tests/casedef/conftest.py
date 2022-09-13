# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_case_definition_json():
    return {
        'id': 'anId',
        'key': 'aKey',
        'category': 'aCategory',
        'name': 'aName',
        'version': 1,
        'resource': 'aResource',
        'deploymentId': 'anotherId',
        'tenantId': 'aTenantId',
        'historyTimeToLive': 10
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
        'resource_name_like': 'aResourceName',
        'tenant_id_in': [1, 2],
        'without_tenant_id': True,
        'include_without_tenant_id': True,
        'sort_by': 'category',
        'ascending': False,
        'first_result': 1,
        'max_results': 10
    }


@pytest.fixture
def getlist_output():
    return {
        'caseDefinitionId': 'anId',
        'caseDefinitionIdIn': [1],
        'name': 'aName',
        'nameLike': 'aNam',
        'deploymentId': 'aDeploymentId',
        'key': 'aKey',
        'keyLike': 'aKe',
        'category': 'aCategory',
        'categoryLike': 'aCategor',
        'version': 1,
        'latestVersion': 'true',
        'resourceName': 'aResourceName',
        'resourceNameLike': 'aResourceName',
        'tenantIdIn': [1, 2],
        'withoutTenantId': 'true',
        'includeCaseDefinitionsWithoutTenantId': 'true',
        'sortBy': 'category',
        'sortOrder': 'desc',
        'firstResult': 1,
        'maxResults': 10
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
        'resource_name_like': 'aResourceNam',
        'tenant_id_in': [1, 2],
        'without_tenant_id': True,
        'include_without_tenant_id': True
    }


@pytest.fixture
def count_output():
    return {
        'caseDefinitionId': 'anId',
        'caseDefinitionIdIn': [1],
        'name': 'aName',
        'nameLike': 'aNam',
        'deploymentId': 'aDeploymentId',
        'key': 'aKey',
        'keyLike': 'aKe',
        'category': 'aCategory',
        'categoryLike': 'aCategor',
        'version': 1,
        'latestVersion': 'true',
        'resourceName': 'aResourceName',
        'resourceNameLike': 'aResourceNam',
        'tenantIdIn': [1, 2],
        'withoutTenantId': 'true',
        'includeCaseDefinitionsWithoutTenantId': 'true'
    }
