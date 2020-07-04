# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processdef
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, response_mock


def test_getxml_params(engine_url):
    get_xml = pycamunda.processdef.GetXML(url=engine_url, id_='anId')

    assert get_xml.url == engine_url + '/process-definition/anId/xml'
    assert get_xml.query_parameters() == {}
    assert get_xml.body_parameters() == {}


def test_getxml_path(engine_url):
    get_xml_id = pycamunda.processdef.GetXML(url=engine_url, id_='anId')
    get_xml_key = pycamunda.processdef.GetXML(url=engine_url, key='aKey')
    get_xml_tenant = pycamunda.processdef.GetXML(url=engine_url, key='aKey', tenant_id='aTenantId')

    assert get_xml_id.url == engine_url + '/process-definition/anId/xml'
    assert get_xml_key.url == engine_url + '/process-definition/key/aKey/xml'
    assert get_xml_tenant.url == engine_url + '/process-definition/key/aKey/tenant-id/aTenantId/xml'


@unittest.mock.patch('requests.Session.request')
def test_getxml_calls_requests(mock, engine_url):
    get_xml = pycamunda.processdef.GetXML(url=engine_url, id_='anId')
    get_xml()

    assert mock.called
    assert mock.call_args[1]['method'] == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getxml_raises_pycamunda_exception(engine_url):
    get_xml = pycamunda.processdef.GetXML(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_xml()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getxml_raises_for_status(mock, engine_url):
    get_xml = pycamunda.processdef.GetXML(url=engine_url, id_='anId')
    get_xml()

    assert mock.called


@unittest.mock.patch('requests.Session.request', response_mock)
def test_getxml_returns_bpmn20Xml(engine_url):
    get_xml = pycamunda.processdef.GetXML(url=engine_url, id_='anId')
    result = get_xml()

    assert result == '<my>test</xml>'
