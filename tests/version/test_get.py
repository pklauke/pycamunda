# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.version
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, version_response_mock


def test_get_params(engine_url):
    get_version = pycamunda.version.Get(url=engine_url)

    assert get_version.url == engine_url + '/version'
    assert get_version.query_parameters() == {}
    assert get_version.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_get_calls_requests(mock, engine_url):
    get_version = pycamunda.version.Get(url=engine_url)
    get_version()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_get_raises_pycamunda_exception(engine_url):
    get_version = pycamunda.version.Get(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_version()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_get_raises_for_status(mock, engine_url):
    get_version = pycamunda.version.Get(url=engine_url)
    get_version()

    assert mock.called


@unittest.mock.patch('requests.Session.request', version_response_mock)
def test_get_returns_string(engine_url):
    get_version = pycamunda.version.Get(url=engine_url)
    version = get_version()

    assert isinstance(version, str)
