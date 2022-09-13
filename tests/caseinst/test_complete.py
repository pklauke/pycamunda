# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.caseinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_complete_params(engine_url):
    complete_instance = pycamunda.caseinst.Complete(url=engine_url, id_='anId', deletions=['aVar'])
    complete_instance.add_variable(
        name='anotherVar', type_='String', value='aVal', value_info={}, local=True
    )

    assert complete_instance.url == engine_url + '/case-instance/anId/complete'
    assert complete_instance.query_parameters() == {}
    assert complete_instance.body_parameters() == {
        'deletions': [{'name': 'aVar'}],
        'variables': {
            'anotherVar': {'value': 'aVal', 'type': 'String', 'valueInfo': {}, 'local': True}
        }
    }


@unittest.mock.patch('requests.Session.request')
def test_complete_calls_requests(mock, engine_url):
    complete_instance = pycamunda.caseinst.Complete(url=engine_url, id_='anId')
    complete_instance()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_complete_raises_pycamunda_exception(engine_url):
    complete_instance = pycamunda.caseinst.Complete(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        complete_instance()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_complete_raises_for_status(mock, engine_url):
    complete_instance = pycamunda.caseinst.Complete(url=engine_url, id_='anId')
    complete_instance()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_complete_returns_none(engine_url):
    complete_instance = pycamunda.caseinst.Complete(url=engine_url, id_='anId')
    result = complete_instance()

    assert result is None
