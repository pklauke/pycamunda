# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.decisiondef
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, response_mock


def test_getdiagram_params(engine_url):
    get_diagram = pycamunda.decisiondef.GetDiagram(url=engine_url, id_='anId')

    assert get_diagram.url == engine_url + '/decision-definition/anId/diagram'
    assert get_diagram.query_parameters() == {}
    assert get_diagram.body_parameters() == {}


def test_getdiagram_path(engine_url):
    get_diagram_id = pycamunda.decisiondef.GetDiagram(url=engine_url, id_='anId')
    get_diagram_key = pycamunda.decisiondef.GetDiagram(url=engine_url, key='aKey')
    get_diagram_tenant = pycamunda.decisiondef.GetDiagram(
        url=engine_url, key='aKey', tenant_id='aTenantId'
    )

    assert get_diagram_id.url == engine_url + '/decision-definition/anId/diagram'
    assert get_diagram_key.url == engine_url + '/decision-definition/key/aKey/diagram'
    assert get_diagram_tenant.url == (
        engine_url + '/decision-definition/key/aKey/tenant-id/aTenantId/diagram'
    )


@unittest.mock.patch('requests.Session.request')
def test_getdiagram_calls_requests(mock, engine_url):
    get_diagram = pycamunda.decisiondef.GetDiagram(url=engine_url, id_='anId')
    get_diagram()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getdiagram_raises_pycamunda_exception(engine_url):
    get_diagram = pycamunda.decisiondef.GetDiagram(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_diagram()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getdiagram_raises_for_status(mock, engine_url):
    get_diagram = pycamunda.decisiondef.GetDiagram(url=engine_url, id_='anId')
    get_diagram()

    assert mock.called


@unittest.mock.patch('requests.Session.request', response_mock)
def test_getdiagram_returns_response_content(engine_url):
    get_diagram = pycamunda.decisiondef.GetDiagram(url=engine_url, id_='anId')
    result = get_diagram()

    assert result == 'content'
