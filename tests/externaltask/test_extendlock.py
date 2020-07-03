# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.externaltask
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_extendlock_params(engine_url):
    extend_task_lock = pycamunda.externaltask.ExtendLock(
        url=engine_url, id_='anId', new_duration=10000, worker_id='1'
    )

    assert extend_task_lock.url == engine_url + '/external-task/anId/extendLock'
    assert extend_task_lock.query_parameters() == {}
    assert extend_task_lock.body_parameters() == {
        'newDuration': 10000,
        'workerId': '1'
    }


@unittest.mock.patch('requests.Session.request')
def test_extendlock_calls_requests(mock, engine_url):
    extend_task_lock = pycamunda.externaltask.ExtendLock(
        url=engine_url, id_='anId', new_duration=10000, worker_id='1'
    )
    extend_task_lock()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_extendlock_raises_pycamunda_exception(engine_url):
    extend_task_lock = pycamunda.externaltask.ExtendLock(
        url=engine_url, id_='anId', new_duration=10000, worker_id='1'
    )
    with pytest.raises(pycamunda.PyCamundaException):
        extend_task_lock()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_extendlock_raises_for_status(mock, engine_url):
    extend_task_lock = pycamunda.externaltask.ExtendLock(
        url=engine_url, id_='anId', new_duration=10000, worker_id='1'
    )
    extend_task_lock()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_extendlock_returns_none(engine_url):
    extend_task_lock = pycamunda.externaltask.ExtendLock(
        url=engine_url, id_='anId', new_duration=10000, worker_id='1'
    )
    result = extend_task_lock()

    assert result is None
