# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processinst
import pycamunda.batch
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_modify_params_default(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters() == {
        'skipCustomListeners': False,
        'skipIoMappings': False,
        'instructions': []
    }


def test_modify_params_non_default(engine_url):
    modify_instance = pycamunda.processinst.Modify(
        url=engine_url,
        id_='anInstanceId',
        skip_custom_listeners=True,
        skip_io_mappings=True
    )

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters() == {
        'skipCustomListeners': True,
        'skipIoMappings': True,
        'instructions': []
    }


def test_modify_params_async(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId', async_=True)

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification-async'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters() == {
        'skipCustomListeners': False,
        'skipIoMappings': False,
        'instructions': []
    }


def test_modify_params_before_activity_instruction(engine_url, variables):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    modify_instance.add_before_activity_instruction(id_='anInstructionId', variables=variables)

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters()['instructions'] == [{
        'type': 'startBeforeActivity', 'activityId': 'anInstructionId', 'variables': variables
    }]


def test_modify_params_after_activity_instruction(engine_url, variables):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    modify_instance.add_after_activity_instruction(id_='anInstructionId', variables=variables)

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters()['instructions'] == [{
        'type': 'startAfterActivity', 'activityId': 'anInstructionId', 'variables': variables
    }]


def test_modify_params_cancel_instruction(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    modify_instance.add_cancel_activity_instruction(id_='anInstructionId')

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters()['instructions'] == [{
        'type': 'cancel', 'activityId': 'anInstructionId'
    }]


def test_modify_params_transition_instruction(engine_url, variables):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    modify_instance.add_transition_instruction(id_='anInstructionId', variables=variables)

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters()['instructions'] == [{
        'type': 'startTransition', 'transitionId': 'anInstructionId', 'variables': variables
    }]


def test_modify_params_cancel_activity_instance_instruction(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    modify_instance.add_cancel_activity_instance_instruction(id_='anInstructionId')

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters()['instructions'] == [{
        'type': 'cancel', 'activityInstanceId': 'anInstructionId'
    }]


def test_modify_params_cancel_transition_instance_instruction(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    modify_instance.add_cancel_transition_instance_instruction(id_='anInstructionId')

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters()['instructions'] == [{
        'type': 'cancel', 'transitionInstanceId': 'anInstructionId'
    }]


def test_modify_params_start_before_ancestor_instance_instruction(engine_url, variables):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    modify_instance.add_start_before_ancestor_activity_instance_instruction(
        id_='anInstructionId',
        variables=variables
    )

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters()['instructions'] == [{
        'type': 'startBeforeActivity',
        'ancestorActivityInstanceId': 'anInstructionId',
        'variables': variables
    }]


def test_modify_params_start_after_ancestor_instance_instruction(engine_url, variables):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    modify_instance.add_start_after_ancestor_activity_instance_instruction(
        id_='anInstructionId',
        variables=variables
    )

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters()['instructions'] == [{
        'type': 'startAfterActivity',
        'ancestorActivityInstanceId': 'anInstructionId',
        'variables': variables
    }]


def test_modify_params_cancel_ancestor_instance_instruction(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    modify_instance.add_cancel_ancestor_activity_instance_instruction(id_='anInstructionId')

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters()['instructions'] == [{
        'type': 'cancel',
        'ancestorActivityInstanceId': 'anInstructionId'
    }]


@unittest.mock.patch('requests.Session.request')
def test_modify_calls_requests(mock, engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    modify_instance()

    assert mock.called
    assert mock.call_args[1]['method'] == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_modify_raises_pycamunda_exception(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    with pytest.raises(pycamunda.PyCamundaException):
        modify_instance()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_modify_raises_for_status(mock, engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    modify_instance()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_modify_returns_none(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    result = modify_instance()

    assert result is None


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_modify_async_returns_batch(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId', async_=True)
    batch = modify_instance()

    assert isinstance(batch, pycamunda.batch.Batch)
