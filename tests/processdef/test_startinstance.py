# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processdef
import pycamunda.processinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_startinstance_params(engine_url):
    start_instance = pycamunda.processdef.StartInstance(
        url=engine_url,
        id_='anId',
        skip_custom_listeners=True,
        skip_io_mappings=True,
        with_variables_in_return=True
    )
    start_instance.add_variable(name='aVar', value='aVal', type_='aType', value_info='anInfo')
    start_instance.add_start_before_activity_instruction(id_='aStartBeforeId')
    start_instance.add_start_after_activity_instruction(id_='aStartAfterId')
    start_instance.add_start_transition_instruction(id_='aTransitionId')

    assert start_instance.url == engine_url + '/process-definition/anId/start'
    assert start_instance.query_parameters() == {}
    assert start_instance.body_parameters() == {
        'skipCustomListeners': True,
        'skipIoMappings': True,
        'withVariablesInReturn': True,
        'startInstructions': [
            {'type': 'startBeforeActivity', 'activityId': 'aStartBeforeId'},
            {'type': 'startAfterActivity', 'activityId': 'aStartAfterId'},
            {'type': 'startTransition', 'transitionId': 'aTransitionId'}
        ],
        'variables': {'aVar': {'value': 'aVal', 'type': 'aType', 'valueInfo': 'anInfo'}}
    }


def test_startinstance_path(engine_url):
    start_instance_id = pycamunda.processdef.StartInstance(
        url=engine_url, id_='anId'
    )
    start_instance_key = pycamunda.processdef.StartInstance(
        url=engine_url, key='aKey'
    )
    start_instance_tenant = pycamunda.processdef.StartInstance(
        url=engine_url, key='aKey', tenant_id='aTenantId'
    )

    assert start_instance_id.url == engine_url + '/process-definition/anId/start'
    assert start_instance_key.url == engine_url + '/process-definition/key/aKey/start'
    assert start_instance_tenant.url == engine_url + '/process-definition/key/aKey' \
                                                     '/tenant-id/aTenantId/start'


@unittest.mock.patch('requests.Session.request')
def test_startinstance_calls_requests(mock, engine_url):
    start_instance = pycamunda.processdef.StartInstance(url=engine_url, id_='anId')
    start_instance()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_startinstance_raises_pycamunda_exception(engine_url):
    start_instance = pycamunda.processdef.StartInstance(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        start_instance()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.processinst.ProcessInstance', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_startinstance_raises_for_status(mock, engine_url):
    start_instance = pycamunda.processdef.StartInstance(url=engine_url, id_='anId')
    start_instance()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_startinstance_returns_activitystats(engine_url):
    start_instance = pycamunda.processdef.StartInstance(url=engine_url, id_='anId')
    instance = start_instance()

    assert isinstance(instance, pycamunda.processinst.ProcessInstance)