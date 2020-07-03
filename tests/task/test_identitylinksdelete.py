# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_identitylinksdelete_params(engine_url):
    delete_link = pycamunda.task.IdentityLinksDelete(
        url=engine_url, task_id='anId', user_id='anotherId', type_='assignee'
    )

    assert delete_link.url == engine_url + '/task/anId/identity-links/delete'
    assert delete_link.query_parameters() == {}
    assert delete_link.body_parameters() == {'userId': 'anotherId', 'type': 'assignee'}


def test_identitylinksdelete_raises_assertion_error(engine_url):
    with pytest.raises(AssertionError):
        pycamunda.task.IdentityLinksDelete(
            url=engine_url, task_id='anId', user_id='anId', group_id='anotherId', type_='assignee'
        )


@unittest.mock.patch('requests.Session.request')
def test_identitylinksdelete_calls_requests(mock, engine_url):
    delete_link = pycamunda.task.IdentityLinksDelete(
        url=engine_url, task_id='anId', user_id='anotherId', type_='assignee'
    )
    delete_link()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_identitylinksdelete_raises_pycamunda_exception(engine_url):
    delete_link = pycamunda.task.IdentityLinksDelete(
        url=engine_url, task_id='anId', user_id='anotherId', type_='assignee'
    )
    with pytest.raises(pycamunda.PyCamundaException):
        delete_link()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_identitylinksdelete_raises_for_status(mock, engine_url):
    delete_link = pycamunda.task.IdentityLinksDelete(
        url=engine_url, task_id='anId', user_id='anotherId', type_='assignee'
    )
    delete_link()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_identitylinksdelete_returns_group(engine_url):
    delete_link = pycamunda.task.IdentityLinksDelete(
        url=engine_url, task_id='anId', user_id='anotherId', type_='assignee'
    )
    result = delete_link()

    assert result is None
