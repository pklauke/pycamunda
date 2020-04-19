# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processdef
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, count_response_mock


def test_count_params(engine_url, count_input, count_output):
    count_definitions = pycamunda.processdef.Count(url=engine_url, **count_input)

    assert count_definitions.url == engine_url + '/process-definition/count'
    assert count_definitions.query_parameters() == count_output
    assert count_definitions.body_parameters() == {}


@unittest.mock.patch('requests.get')
def test_count_calls_requests(mock, engine_url):
    count_definitions = pycamunda.processdef.Count(url=engine_url, id_='anId')
    count_definitions()

    assert mock.called


@unittest.mock.patch('requests.get', raise_requests_exception_mock)
def test_count_raises_pycamunda_exception(engine_url):
    count_definitions = pycamunda.processdef.Count(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        count_definitions()


@unittest.mock.patch('requests.get', not_ok_response_mock)
@unittest.mock.patch('pycamunda.processdef.ActivityStats', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_count_raises_for_status(mock, engine_url):
    count_definitions = pycamunda.processdef.Count(url=engine_url, id_='anId')
    count_definitions()

    assert mock.called


@unittest.mock.patch('requests.get', count_response_mock)
def test_count_returns_response_content(engine_url):
    count_definitions = pycamunda.processdef.Count(url=engine_url, id_='anId')
    result = count_definitions()

    assert isinstance(result, int)
