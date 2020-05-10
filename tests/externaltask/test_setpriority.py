# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.externaltask
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_setpriority_params(engine_url):
    set_priority = pycamunda.externaltask.SetPriority(url=engine_url, id_='anId', priority=10)

    assert set_priority.url == engine_url + '/external-task/anId/priority'
    assert set_priority.query_parameters() == {}
    assert set_priority.body_parameters() == {'priority': 10}


@unittest.mock.patch('requests.put')
def test_setpriority_calls_requests(mock, engine_url):
    set_priority = pycamunda.externaltask.SetPriority(url=engine_url, id_='anId', priority=10)
    set_priority()

    assert mock.called


@unittest.mock.patch('requests.put', raise_requests_exception_mock)
def test_setpriority_raises_pycamunda_exception(engine_url):
    set_priority = pycamunda.externaltask.SetPriority(url=engine_url, id_='anId', priority=10)
    with pytest.raises(pycamunda.PyCamundaException):
        set_priority()


@unittest.mock.patch('requests.put', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_setpriority_raises_for_status(mock, engine_url):
    set_priority = pycamunda.externaltask.SetPriority(url=engine_url, id_='anId', priority=10)
    set_priority()

    assert mock.called


@unittest.mock.patch('requests.put', unittest.mock.MagicMock())
def test_setpriority_returns_none(engine_url):
    set_priority = pycamunda.externaltask.SetPriority(url=engine_url, id_='anId', priority=10)
    result = set_priority()

    assert result is None
