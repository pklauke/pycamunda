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
