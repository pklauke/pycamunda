# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.group
import pycamunda.resource
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_options_params(engine_url):
    group_options = pycamunda.group.Options(url=engine_url, id_='anId')

    assert group_options.url == engine_url + '/group/anId'
    assert group_options.query_parameters() == {}
    assert group_options.body_parameters() == {}


@unittest.mock.patch('pycamunda.resource.ResourceOptions.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_options_calls_requests(mock, engine_url):
    group_options = pycamunda.group.Options(url=engine_url, id_='anId')
    group_options()

    assert mock.called
    assert mock.call_args[1]['method'] == 'OPTIONS'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_options_raises_pycamunda_exception(engine_url):
    group_options = pycamunda.group.Options(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        group_options()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.resource.ResourceOptions', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_options_raises_for_status(mock, engine_url):
    group_options = pycamunda.group.Options(url=engine_url, id_='anId')
    group_options()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_options_returns_group(engine_url):
    group_options = pycamunda.group.Options(url=engine_url, id_='anId')
    options = group_options()

    assert isinstance(options, pycamunda.resource.ResourceOptions)
