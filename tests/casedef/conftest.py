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
