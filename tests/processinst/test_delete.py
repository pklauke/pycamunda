# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_delete_params(engine_url, delete_input, delete_output):
    delete_instance = pycamunda.processinst.Delete(url=engine_url, **delete_input)

    assert delete_instance.url == engine_url + '/process-instance/anId'
    assert delete_instance.query_parameters() == delete_output
    assert delete_instance.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_delete_calls_requests(mock, engine_url, delete_input):
    delete_instance = pycamunda.processinst.Delete(url=engine_url, **delete_input)
    delete_instance()

    assert mock.called
    assert mock.call_args[1]['method'] == 'DELETE'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_delete_raises_pycamunda_exception(engine_url, delete_input):
    delete_instance = pycamunda.processinst.Delete(url=engine_url, **delete_input)
    with pytest.raises(pycamunda.PyCamundaException):
        delete_instance()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_delete_raises_for_status(mock, engine_url, delete_input):
    delete_instance = pycamunda.processinst.Delete(url=engine_url, **delete_input)
    delete_instance()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_delete_returns_none(engine_url, delete_input):
    delete_instance = pycamunda.processinst.Delete(url=engine_url, **delete_input)
    result = delete_instance()

    assert result is None
