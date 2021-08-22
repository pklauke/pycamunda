# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.caseinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_get_params(engine_url):
    get_instance = pycamunda.caseinst.Get(url=engine_url, id_='anId')

    assert get_instance.url == engine_url + '/case-instance/anId'
    assert get_instance.query_parameters() == {}
    assert get_instance.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_get_calls_requests(mock, engine_url):
    get_instance = pycamunda.caseinst.Get(url=engine_url, id_='anId')
    get_instance()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_get_raises_pycamunda_exception(engine_url):
    get_instance = pycamunda.caseinst.Get(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_instance()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.caseinst.CaseInstance', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_get_raises_for_status(mock, engine_url):
    get_instance = pycamunda.caseinst.Get(url=engine_url, id_='anId')
    get_instance()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_get_returns_casedefinition(engine_url):
    get_instance = pycamunda.caseinst.Get(url=engine_url, id_='anId')
    case_instance = get_instance()

    assert isinstance(case_instance, pycamunda.caseinst.CaseInstance)
