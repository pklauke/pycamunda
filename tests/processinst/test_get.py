# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_get_params(engine_url):
    get_instance = pycamunda.processinst.Get(url=engine_url, id_='anProcessInstanceId')

    assert get_instance.url == engine_url + '/process-instance/anProcessInstanceId'
    assert get_instance.query_parameters() == {}
    assert get_instance.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
@unittest.mock.patch('pycamunda.processinst.ProcessInstance', unittest.mock.MagicMock())
def test_get_calls_requests(mock, engine_url):
    get_instance = pycamunda.processinst.Get(url=engine_url, id_='anProcessInstanceId')
    get_instance()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_get_raises_pycamunda_exception(engine_url):
    get_instance = pycamunda.processinst.Get(url=engine_url, id_='anProcessInstanceId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_instance()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.processinst.ProcessInstance', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_get_raises_for_status(mock, engine_url):
    get_instance = pycamunda.processinst.Get(url=engine_url, id_='anProcessInstanceId')
    get_instance()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_get_returns_none(engine_url):
    get_instance = pycamunda.processinst.Get(url=engine_url, id_='anProcessInstanceId')
    instance = get_instance()

    assert isinstance(instance, pycamunda.processinst.ProcessInstance)
