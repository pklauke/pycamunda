# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.tenant
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_groupmemberdelete_params(engine_url):
    delete_member = pycamunda.tenant.GroupMemberDelete(
        url=engine_url, id_='anId', group_id='anotherId'
    )

    assert delete_member.url == engine_url + '/tenant/anId/group-members/anotherId'
    assert delete_member.query_parameters() == {}
    assert delete_member.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_groupmemberdelete_calls_requests(mock, engine_url):
    delete_member = pycamunda.tenant.GroupMemberDelete(
        url=engine_url, id_='anId', group_id='anotherId'
    )
    delete_member()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'DELETE'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_groupmemberdelete_raises_pycamunda_exception(engine_url):
    delete_member = pycamunda.tenant.GroupMemberDelete(
        url=engine_url, id_='anId', group_id='anotherId'
    )

    with pytest.raises(pycamunda.PyCamundaException):
        delete_member()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_groupmemberdelete_raises_for_status(mock, engine_url):
    delete_member = pycamunda.tenant.GroupMemberDelete(
        url=engine_url, id_='anId', group_id='anotherId'
    )
    delete_member()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_groupmemberdelete_returns_none(engine_url):
    delete_member = pycamunda.tenant.GroupMemberDelete(
        url=engine_url, id_='anId', group_id='anotherId'
    )
    result = delete_member()

    assert result is None
