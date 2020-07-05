# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.group
import pycamunda.resource
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_memberoptions_params(engine_url):
    member_options = pycamunda.group.MemberOptions(url=engine_url, id_='anId')

    assert member_options.url == engine_url + '/group/anId/members'
    assert member_options.query_parameters() == {}
    assert member_options.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_memberoptions_calls_requests(mock, engine_url):
    member_options = pycamunda.group.MemberOptions(url=engine_url, id_='anId')
    member_options()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'OPTIONS'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_memberoptions_raises_pycamunda_exception(engine_url):
    member_options = pycamunda.group.MemberOptions(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        member_options()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.resource.ResourceOptions', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_memberoptions_raises_for_status(mock, engine_url):
    member_options = pycamunda.group.MemberOptions(url=engine_url, id_='anId')
    member_options()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_memberoptions_returns_none(engine_url):
    member_options = pycamunda.group.MemberOptions(url=engine_url, id_='anId')
    options = member_options()

    assert isinstance(options, pycamunda.resource.ResourceOptions)
