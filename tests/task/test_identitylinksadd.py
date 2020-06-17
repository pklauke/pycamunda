# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_identitylinksadd_params(engine_url):
    add_link = pycamunda.task.IdentityLinksAdd(
        url=engine_url, task_id='anId', user_id='anotherId', type_='assignee'
    )

    assert add_link.url == engine_url + '/task/anId/identity-links'
    assert add_link.query_parameters() == {}
    assert add_link.body_parameters() == {'userId': 'anotherId', 'type': 'assignee'}


def test_identitylinksadd_raises_assertion_error(engine_url):
    with pytest.raises(AssertionError):
        pycamunda.task.IdentityLinksAdd(
            url=engine_url, task_id='anId', user_id='anId', group_id='anotherId', type_='assignee'
        )


@unittest.mock.patch('requests.post')
def test_identitylinksadd_calls_requests(mock, engine_url):
    add_link = pycamunda.task.IdentityLinksAdd(
        url=engine_url, task_id='anId', user_id='anotherId', type_='assignee'
    )
    add_link()

    assert mock.called


@unittest.mock.patch('requests.post', raise_requests_exception_mock)
def test_identitylinksadd_raises_pycamunda_exception(engine_url):
    add_link = pycamunda.task.IdentityLinksAdd(
        url=engine_url, task_id='anId', user_id='anotherId', type_='assignee'
    )
    with pytest.raises(pycamunda.PyCamundaException):
        add_link()


@unittest.mock.patch('requests.post', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_identitylinksadd_raises_for_status(mock, engine_url):
    add_link = pycamunda.task.IdentityLinksAdd(
        url=engine_url, task_id='anId', user_id='anotherId', type_='assignee'
    )
    add_link()

    assert mock.called


@unittest.mock.patch('requests.post', unittest.mock.MagicMock())
def test_identitylinksadd_returns_group(engine_url):
    add_link = pycamunda.task.IdentityLinksAdd(
        url=engine_url, task_id='anId', user_id='anotherId', type_='assignee'
    )
    result = add_link()

    assert result is None
