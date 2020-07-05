# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processdef
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, response_mock


def test_getprocessdiagram_params(engine_url):
    get_process_diagram = pycamunda.processdef.GetProcessDiagram(url=engine_url, id_='anId')

    assert get_process_diagram.url == engine_url + '/process-definition/anId/diagram'
    assert get_process_diagram.query_parameters() == {}
    assert get_process_diagram.body_parameters() == {}


def test_getprocessdiagram_path(engine_url):
    get_process_diagram_id = pycamunda.processdef.GetProcessDiagram(url=engine_url, id_='anId')
    get_process_diagram_key = pycamunda.processdef.GetProcessDiagram(url=engine_url, key='aKey')
    get_process_diagram_tenant = pycamunda.processdef.GetProcessDiagram(
        url=engine_url, key='aKey', tenant_id='aTenantId'
    )

    assert get_process_diagram_id.url == engine_url + '/process-definition/anId/diagram'
    assert get_process_diagram_key.url == engine_url + '/process-definition/key/aKey/diagram'
    assert get_process_diagram_tenant.url == engine_url + '/process-definition/key/aKey' \
                                                          '/tenant-id/aTenantId/diagram'


@unittest.mock.patch('requests.Session.request')
def test_getprocessdiagram_calls_requests(mock, engine_url):
    get_process_diagram = pycamunda.processdef.GetProcessDiagram(url=engine_url, id_='anId')
    get_process_diagram()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getprocessdiagram_raises_pycamunda_exception(engine_url):
    get_process_diagram = pycamunda.processdef.GetProcessDiagram(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_process_diagram()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.processdef.ActivityStats', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getprocessdiagram_raises_for_status(mock, engine_url):
    get_process_diagram = pycamunda.processdef.GetProcessDiagram(url=engine_url, id_='anId')
    get_process_diagram()

    assert mock.called


@unittest.mock.patch('requests.Session.request', response_mock)
def test_getprocessdiagram_returns_response_content(engine_url):
    get_process_diagram = pycamunda.processdef.GetProcessDiagram(url=engine_url, id_='anId')
    result = get_process_diagram()

    assert result == 'content'
