# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_identitylinksgetlist_params(engine_url):
    get_links = pycamunda.task.IdentityLinksGetList(url=engine_url, task_id='anId', type_='assignee')

    assert get_links.url == engine_url + '/task/anId/identity-links'
    assert get_links.query_parameters() == {'type': 'assignee'}
    assert get_links.body_parameters() == {}


@unittest.mock.patch('pycamunda.task.IdentityLink.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_identitylinksgetlist_calls_requests(mock, engine_url):
    get_links = pycamunda.task.IdentityLinksGetList(url=engine_url)
    get_links()

    assert mock.called
    assert mock.call_args[1]['method'] == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_identitylinksgetlist_raises_pycamunda_exception(engine_url):
    get_links = pycamunda.task.IdentityLinksGetList(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_links()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.task.IdentityLink', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_identitylinksgetlist_raises_for_status(mock, engine_url):
    get_links = pycamunda.task.IdentityLinksGetList(url=engine_url)
    get_links()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_identitylinksgetlist_returns_group(engine_url):
    get_links = pycamunda.task.IdentityLinksGetList(url=engine_url)
    links = get_links()

    assert isinstance(links, tuple)
    assert all(isinstance(link, pycamunda.task.IdentityLink) for link in links)
