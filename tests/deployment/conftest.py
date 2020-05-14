# -*- coding: utf-8 -*-

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
