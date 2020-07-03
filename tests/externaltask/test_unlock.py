# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.externaltask
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_unlock_params(engine_url):
    unlock_task = pycamunda.externaltask.Unlock(url=engine_url, id_='anId')

    assert unlock_task.url == engine_url + '/external-task/anId/unlock'
    assert unlock_task.query_parameters() == {}
    assert unlock_task.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_unlock_calls_requests(mock, engine_url):
    unlock_task = pycamunda.externaltask.Unlock(url=engine_url, id_='anId')
    unlock_task()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_unlock_raises_pycamunda_exception(engine_url):
    unlock_task = pycamunda.externaltask.Unlock(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        unlock_task()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_unlock_raises_for_status(mock, engine_url):
    unlock_task = pycamunda.externaltask.Unlock(url=engine_url, id_='anId')
    unlock_task()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_unlock_returns_none(engine_url):
    unlock_task = pycamunda.externaltask.Unlock(url=engine_url, id_='anId')
    result = unlock_task()

    assert result is None
