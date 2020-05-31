# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_update_params(engine_url, update_input, update_output):
    update_task = pycamunda.task.Update(url=engine_url, id_='anId', **update_input)

    assert update_task.url == engine_url + '/task/anId'
    assert update_task.query_parameters() == {}
    assert update_task.body_parameters() == update_output


@unittest.mock.patch('requests.put')
def test_update_calls_requests(mock, engine_url, update_input):
    update_task = pycamunda.task.Update(url=engine_url, id_='anId', **update_input)
    update_task()

    assert mock.called


@unittest.mock.patch('requests.put', raise_requests_exception_mock)
def test_update_raises_pycamunda_exception(engine_url, update_input):
    update_task = pycamunda.task.Update(url=engine_url, id_='anId', **update_input)
    with pytest.raises(pycamunda.PyCamundaException):
        update_task()


@unittest.mock.patch('requests.put', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_update_raises_for_status(mock, engine_url, update_input):
    update_task = pycamunda.task.Update(url=engine_url, id_='anId', **update_input)
    update_task()

    assert mock.called


@unittest.mock.patch('requests.put', unittest.mock.MagicMock())
def test_update_returns_none(engine_url, update_input):
    update_task = pycamunda.task.Update(url=engine_url, id_='anId', **update_input)
    result = update_task()

    assert result is None
