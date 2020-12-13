# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_decision_definition_json():
    return {
        'id': 'anId',
        'key': 'aKey',
        'category': 'aCategory',
        'name': 'aName',
        'version': 1,
        'resource': 'aResource',
        'deploymentId': 'aDeploymentId',
        'decisionRequirementsDefinitionId': 'anotherId',
        'decisionRequirementsDefinitionKey': 'justAnotherId',
        'tenantId': 'aTenantId',
        'versionTag': 'aTag',
        'historyTimeToLive': 10
    }
