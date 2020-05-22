# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.group
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_membercreate_params(engine_url):
    create_member = pycamunda.group.MemberCreate(url=engine_url, id_='anId', user_id='anUserId')

    assert create_member.url == engine_url + '/group/anId/members/anUserId'
    assert create_member.query_parameters() == {}
    assert create_member.body_parameters() == {}


@unittest.mock.patch('requests.put')
def test_membercreate_calls_requests(mock, engine_url):
    create_member = pycamunda.group.MemberCreate(url=engine_url, id_='anId', user_id='anUserId')
    create_member()

    assert mock.called


@unittest.mock.patch('requests.put', raise_requests_exception_mock)
def test_membercreate_raises_pycamunda_exception(engine_url):
    create_member = pycamunda.group.MemberCreate(url=engine_url, id_='anId', user_id='anUserId')
    with pytest.raises(pycamunda.PyCamundaException):
        create_member()


@unittest.mock.patch('requests.put', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_membercreate_raises_for_status(mock, engine_url):
    create_member = pycamunda.group.MemberCreate(url=engine_url, id_='anId', user_id='anUserId')
    create_member()

    assert mock.called


@unittest.mock.patch('requests.put', unittest.mock.MagicMock())
def test_membercreate_returns_none(engine_url):
    create_member = pycamunda.group.MemberCreate(url=engine_url, id_='anId', user_id='anUserId')
    result = create_member()

    assert result is None
