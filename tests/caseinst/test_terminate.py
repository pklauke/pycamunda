# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.caseinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_terminate_params(engine_url):
    terminate_instance = pycamunda.caseinst.Terminate(
        url=engine_url, id_='anId', deletions=['aVar']
    )
    terminate_instance.add_variable(
        name='anotherVar', type_='String', value='aVal', value_info={}, local=True
    )

    assert terminate_instance.url == engine_url + '/case-instance/anId/terminate'
    assert terminate_instance.query_parameters() == {}
    assert terminate_instance.body_parameters() == {
        'deletions': [{'name': 'aVar'}],
        'variables': {
            'anotherVar': {'value': 'aVal', 'type': 'String', 'valueInfo': {}, 'local': True}
        }
    }


@unittest.mock.patch('requests.Session.request')
def test_terminate_calls_requests(mock, engine_url):
    terminate_instance = pycamunda.caseinst.Terminate(url=engine_url, id_='anId')
    terminate_instance()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_terminate_raises_pycamunda_exception(engine_url):
    terminate_instance = pycamunda.caseinst.Terminate(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        terminate_instance()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_terminate_raises_for_status(mock, engine_url):
    terminate_instance = pycamunda.caseinst.Terminate(url=engine_url, id_='anId')
    terminate_instance()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_terminate_returns_none(engine_url):
    terminate_instance = pycamunda.caseinst.Terminate(url=engine_url, id_='anId')
    result = terminate_instance()

    assert result is None
