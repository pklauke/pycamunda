# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def my_batch_json():
    return {
        'id': 'anId',
        'type': 'aType',
        'totalJobs': 1,
        'jobsCreated': 2,
        'batchJobsPerSeed': 3,
        'invocationsPerBatchJob': 4,
        'seedJobDefinitionId': 'aSeedId',
        'monitorJobDefinitionId': 'aMonitorId',
        'batchJobDefinitionId': 'aBatchId',
        'suspended': True,
        'tenantId': 'aTenantId',
        'createUserId': 'anUserId'
    }


@pytest.fixture
def my_batchstats_json():
    return {
        'id': 'anId',
        'type': 'aType',
        'totalJobs': 1,
        'jobsCreated': 2,
        'batchJobsPerSeed': 3,
        'invocationsPerBatchJob': 4,
        'seedJobDefinitionId': 'aSeedId',
        'monitorJobDefinitionId': 'aMonitorId',
        'batchJobDefinitionId': 'aBatchId',
        'suspended': True,
        'tenantId': 'aTenantId',
        'createUserId': 'anUserId',
        'remainingJobs': 5,
        'completedJobs': 6,
        'failedJobs': 7
    }


@pytest.fixture
def getlist_input():
    return {
        'batch_id': 'anId',
        'type_': 'aType',
        'tenant_id_in': ['aTenantId'],
        'without_tenant_id': True,
        'suspended': True,
        'sort_by': 'batch_id',
        'ascending': True,
        'first_result': 1,
        'max_results': 10
    }


@pytest.fixture
def getlist_output():
    return {
        'batchId': 'anId',
        'type': 'aType',
        'tenantIdIn': ['aTenantId'],
        'withoutTenantId': 'true',
        'suspended': 'true',
        'sortBy': 'batchId',
        'sortOrder': 'asc',
        'firstResult': 1,
        'maxResults': 10
    }


@pytest.fixture
def count_input():
    return {
        'batch_id': 'anId',
        'type_': 'aType',
        'tenant_id_in': ['aTenantId'],
        'without_tenant_id': True,
        'suspended': True
    }


@pytest.fixture
def count_output():
    return {
        'batchId': 'anId',
        'type': 'aType',
        'tenantIdIn': ['aTenantId'],
        'withoutTenantId': 'true',
        'suspended': 'true'
    }
