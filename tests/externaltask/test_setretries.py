# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.externaltask
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_setretries_params(engine_url):
    set_retries = pycamunda.externaltask.SetRetries(url=engine_url, id_='anId', retries=10)

    assert set_retries.url == engine_url + '/external-task/anId/retries'
    assert set_retries.query_parameters() == {}
    assert set_retries.body_parameters() == {'retries': 10}


@unittest.mock.patch('requests.put')
def test_setretries_calls_requests(mock, engine_url):
    set_retries = pycamunda.externaltask.SetRetries(url=engine_url, id_='anId', retries=10)
    set_retries()

    assert mock.called


@unittest.mock.patch('requests.put', raise_requests_exception_mock)
def test_setretries_raises_pycamunda_exception(engine_url):
    set_retries = pycamunda.externaltask.SetRetries(url=engine_url, id_='anId', retries=10)
    with pytest.raises(pycamunda.PyCamundaException):
        set_retries()


@unittest.mock.patch('requests.put', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_setretries_raises_for_status(mock, engine_url):
    set_retries = pycamunda.externaltask.SetRetries(url=engine_url, id_='anId', retries=10)
    set_retries()

    assert mock.called


@unittest.mock.patch('requests.put', unittest.mock.MagicMock())
def test_setretries_returns_none(engine_url):
    set_retries = pycamunda.externaltask.SetRetries(url=engine_url, id_='anId', retries=10)
    result = set_retries()

    assert result is None
