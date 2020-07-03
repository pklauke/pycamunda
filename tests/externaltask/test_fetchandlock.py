# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.externaltask
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_fetchandlock_params(engine_url):
    fetch_and_lock = pycamunda.externaltask.FetchAndLock(
        url=engine_url, worker_id='1', max_tasks=10, use_priority=True
    )
    fetch_and_lock.add_topic(
        name='aTopic', lock_duration=10000, variables=['aVar'], deserialize_values=False
    )

    assert fetch_and_lock.url == engine_url + '/external-task/fetchAndLock'
    assert fetch_and_lock.query_parameters() == {}
    assert fetch_and_lock.body_parameters() == {
        'workerId': '1',
        'maxTasks': 10,
        'usePriority': True,
        'topics': [{
            'topicName': 'aTopic',
            'lockDuration': 10000,
            'variables': ['aVar'],
            'deserializeValues': False
        }]
    }


@unittest.mock.patch('requests.Session.request')
def test_fetchandlock_calls_requests(mock, engine_url):
    fetch_and_lock = pycamunda.externaltask.FetchAndLock(
        url=engine_url, worker_id='1', max_tasks=10
    )
    fetch_and_lock()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_fetchandlock_raises_pycamunda_exception(engine_url):
    fetch_and_lock = pycamunda.externaltask.FetchAndLock(
        url=engine_url, worker_id='1', max_tasks=10
    )
    with pytest.raises(pycamunda.PyCamundaException):
        fetch_and_lock()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.externaltask.ExternalTask', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_fetchandlock_raises_for_status(mock, engine_url):
    fetch_and_lock = pycamunda.externaltask.FetchAndLock(
        url=engine_url, worker_id='1', max_tasks=10
    )
    fetch_and_lock()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_fetchandlock_returns_tuple(engine_url):
    fetch_and_lock = pycamunda.externaltask.FetchAndLock(
        url=engine_url, worker_id='1', max_tasks=10
    )
    tasks = fetch_and_lock()

    assert isinstance(tasks, tuple)
    assert all(isinstance(task, pycamunda.externaltask.ExternalTask) for task in tasks)
