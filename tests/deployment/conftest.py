# -*- coding: utf-8 -*-

import datetime as dt

import pytest


@pytest.fixture
def my_deployment_json():
    return {
        'id': 'anId',
        'name': 'aName',
        'source': 'aSource',
        'tenantId': 'aTenantId',
        'deploymentTime': '2000-01-01T00:00:00.000+0000'
    }


@pytest.fixture
def getlist_input():
    return {
        'id_': 'anId',
        'name': 'aName',
        'name_like': 'aNam',
        'source': 'aSource',
        'without_source': True,
        'tenant_id_in': [],
        'without_tenant_id': True,
        'include_deployments_without_tenant_id': True,
        'after': dt.datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0,
                             tzinfo=dt.timezone.utc),
        'before': dt.datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0,
                              tzinfo=dt.timezone.utc),
        'sort_by': 'id_',
        'ascending': True,
        'first_result': 1,
        'max_results': 10
    }


@pytest.fixture
def getlist_output():
    return {
        'id': 'anId',
        'name': 'aName',
        'nameLike': 'aNam',
        'source': 'aSource',
        'withoutSource': 'true',
        'tenantIdIn': [],
        'withoutTenantId': 'true',
        'includeDeploymentsWithoutTenantId': 'true',
        'after': '2000-01-01T00:00:00.000+0000',
        'before': '2000-01-01T00:00:00.000+0000',
        'sortBy': 'id',
        'sortOrder': 'asc',
        'firstResult': 1,
        'maxResults': 10
    }


@pytest.fixture
def create_input():
    return {
        'name': 'aName',
        'source': 'aSource',
        'enable_duplicate_filtering': True,
        'deploy_changed_only': True,
        'tenant_id': 'aTenantId'
    }


@pytest.fixture
def create_output():
    return {
        'deployment-name': 'aName',
        'deployment-source': 'aSource',
        'enable-duplicate-filtering': True,
        'deploy-changed-only': True,
        'tenant-id': 'aTenantId'
    }


@pytest.fixture
def my_depl_with_def_json():
    return {
        'links': [],
        'id': 'anId',
        'name': 'aName',
        'source': 'aSource',
        'deployedProcessDefinitions': {},
        'deployedCaseDefinitions': {},
        'deployedDecisionDefinitions': {},
        'deployedDecisionRequirementsDefinitions': {},
        'tenantId': 'aTenantId',
        'deploymentTime': '2020-01-01T00:00:00.000+0000'
    }
