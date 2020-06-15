# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_execution_json():
    return {
        'id': 'anId', 'processInstanceId': 'anInstanceId', 'ended': True, 'tenantId': 'aTenantId'
    }
