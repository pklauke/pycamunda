# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_process_instance_json():
    return {
        'id': 'anId',
        'definitionId': 'anDefinitionId',
        'businessKey': 'aBusinessKey',
        'caseInstanceId': 'aCaseInstanceId',
        'suspended': False,
        'tenantId': 'aTenantId',
        'links': []
    }


@pytest.fixture
def delete_input():
    return {
        'id_': 'anId',
        'skip_custom_listeners': False,
        'skip_io_mappings': False,
        'skip_subprocesses': False,
        'fail_if_not_exists': False
    }


@pytest.fixture
def delete_output():
    return {
        'skipCustomListeners': False,
        'skipIoMappings': False,
        'skipSubprocesses': False,
        'failIfNotExists': False
    }
