# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getlist_params(engine_url, getlist_input, getlist_output):
    get_instances = pycamunda.processinst.GetList(url=engine_url, **getlist_input)

    assert get_instances.url == engine_url + '/process-instance'
    assert get_instances.query_parameters() == getlist_output
    assert get_instances.body_parameters() == {}


@unittest.mock.patch('requests.get')
@unittest.mock.patch('pycamunda.processinst.ProcessInstance', unittest.mock.MagicMock())
def test_getlist_calls_requests(mock, engine_url):
    get_instances = pycamunda.processinst.GetList(url=engine_url)
    get_instances()

    assert mock.called


@unittest.mock.patch('requests.get', raise_requests_exception_mock)
def test_getlist_raises_pycamunda_exception(engine_url):
    get_instances = pycamunda.processinst.GetList(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_instances()


@unittest.mock.patch('requests.get', not_ok_response_mock)
@unittest.mock.patch('pycamunda.processinst.ProcessInstance', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getlist_raises_for_status(mock, engine_url):
    get_instances = pycamunda.processinst.GetList(url=engine_url)
    get_instances()

    assert mock.called


@unittest.mock.patch('requests.get', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.processinst.ProcessInstance', unittest.mock.MagicMock())
def test_getlist_returns_none(engine_url):
    get_instances = pycamunda.processinst.GetList(url=engine_url)
    users = get_instances()

    assert isinstance(users, tuple)
