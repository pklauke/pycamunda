# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processdef
import pycamunda.processinst
import pycamunda.batch
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_restartprocessinstance_params(
    engine_url, restartprocessinstance_input, restartprocessinstance_output
):
    restart_instance = pycamunda.processdef.RestartProcessInstance(
        url=engine_url, **restartprocessinstance_input
    )
    restart_instance.add_before_activity_instruction(id_='aStartBeforeId')
    restart_instance.add_after_activity_instruction(id_='aStartAfterId')
    restart_instance.add_transition_instruction(id_='aTransitionId')

    restart_instance_async = pycamunda.processdef.RestartProcessInstance(
        url=engine_url, id_='anId', process_instance_ids=[], async_=True
    )

    assert restart_instance.url == engine_url + '/process-definition/anId/restart'
    assert restart_instance.query_parameters() == {}
    assert restart_instance.body_parameters() == {
        **restartprocessinstance_output,
        'instructions': [{
            'activityId': 'aStartBeforeId',
            'type': 'startBeforeActivity'
        }, {
            'activityId': 'aStartAfterId',
            'type': 'startAfterActivity'
        }, {
            'transitionId': 'aTransitionId',
            'type': 'startTransition'
        }]
    }
    assert restart_instance_async.url == engine_url + '/process-definition/anId/restart-async'


@unittest.mock.patch('requests.post')
def test_restartprocessinstance_calls_requests(mock, engine_url):
    start_instance = pycamunda.processdef.RestartProcessInstance(
        url=engine_url, id_='anId', process_instance_ids=[]
    )
    start_instance()

    assert mock.called


@unittest.mock.patch('requests.post', raise_requests_exception_mock)
def test_restartprocessinstance_raises_pycamunda_exception(engine_url):
    restart_instance = pycamunda.processdef.RestartProcessInstance(
        url=engine_url, id_='anId', process_instance_ids=[]
    )
    with pytest.raises(pycamunda.PyCamundaException):
        restart_instance()


@unittest.mock.patch('requests.post', not_ok_response_mock)
@unittest.mock.patch('pycamunda.processinst.ProcessInstance', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_restartprocessinstance_raises_for_status(mock, engine_url):
    restart_instance = pycamunda.processdef.RestartProcessInstance(
        url=engine_url, id_='anId', process_instance_ids=[]
    )
    restart_instance()

    assert mock.called


@unittest.mock.patch('requests.post', unittest.mock.MagicMock())
def test_restartprocessinstance_returns_none(engine_url):
    restart_instance = pycamunda.processdef.RestartProcessInstance(
        url=engine_url, id_='anId', process_instance_ids=[]
    )
    result = restart_instance()

    assert result is None


@unittest.mock.patch('requests.post', unittest.mock.MagicMock())
def test_restartprocessinstance_async_returns_batch(engine_url):
    restart_instance = pycamunda.processdef.RestartProcessInstance(
        url=engine_url, id_='anId', process_instance_ids=[], async_=True
    )
    batch = restart_instance()

    assert isinstance(batch, pycamunda.batch.Batch)
