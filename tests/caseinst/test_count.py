# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.caseinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, count_response_mock


def test_count_params(engine_url, count_input, count_output):
    count_instances = pycamunda.caseinst.Count(url=engine_url, **count_input)

    assert count_instances.url == engine_url + '/case-instance/count'
    assert count_instances.query_parameters() == count_output
    assert count_instances.body_parameters() == {}


def test_count_variable_params(engine_url):
    count_instances = pycamunda.caseinst.Count(url=engine_url)

    count_instances.add_variable(name='myvar', value='myval', type_='type', value_info={})

    assert count_instances.query_parameters() == {
        'variables': {'myvar': {'value': 'myval', 'type': 'type', 'valueInfo': {}}}
    }


@unittest.mock.patch('requests.Session.request')
def test_count_calls_requests(mock, engine_url):
    count_instances = pycamunda.caseinst.Count(url=engine_url)
    count_instances()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_count_raises_pycamunda_exception(engine_url):
    count_instances = pycamunda.caseinst.Count(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        count_instances()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.caseinst.CaseInstance', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_count_raises_for_status(mock, engine_url):
    count_instances = pycamunda.caseinst.Count(url=engine_url)
    count_instances()

    assert mock.called


@unittest.mock.patch('requests.Session.request', count_response_mock)
def test_count_returns_int(engine_url):
    count_instances = pycamunda.caseinst.Count(url=engine_url)
    result = count_instances()

    assert isinstance(result, int)
