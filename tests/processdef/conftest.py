# -*- coding: utf-8 -*-

import pytest

import pycamunda.variable


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
        'incidents': []
    }
