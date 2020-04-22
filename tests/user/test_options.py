# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.user
import pycamunda.resource
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_options_params(engine_url):
    get_options = pycamunda.user.Options(url=engine_url, id_='myuserid')

    assert get_options.url == engine_url + '/user/myuserid'
    assert get_options.query_parameters() == {}
    assert get_options.body_parameters() == {}


@unittest.mock.patch('requests.options')
def test_options_calls_requests(mock, engine_url):
    get_options = pycamunda.user.Options(url=engine_url, id_='myuserid')
    get_options()

    assert mock.called


@unittest.mock.patch('requests.options', raise_requests_exception_mock)
def test_options_raises_pycamunda_exception(engine_url):
    get_options = pycamunda.user.Options(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_options()


@unittest.mock.patch('requests.options', not_ok_response_mock)
@unittest.mock.patch('pycamunda.resource.ResourceOptions', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_options_raises_for_status(mock, engine_url):
    get_options = pycamunda.user.Options(url=engine_url, id_='myuserid')
    get_options()

    assert mock.called


@unittest.mock.patch('requests.options', unittest.mock.MagicMock())
def test_options_returns_resource_options(engine_url):
    get_options = pycamunda.user.Options(url=engine_url, id_='myuserid')
    resource_options = get_options()

    assert isinstance(resource_options, pycamunda.resource.ResourceOptions)