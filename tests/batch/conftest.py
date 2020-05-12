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
