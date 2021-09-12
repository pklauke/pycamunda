# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.decisiondef
import pycamunda.variable
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_evaluate_params(engine_url):
    evaluate = pycamunda.decisiondef.Evaluate(url=engine_url, id_='anId')
    evaluate.add_variable(name='aVar', value='aVal', type_='aType', value_info='anInfo')

    assert evaluate.url == engine_url + '/decision-definition/anId/evaluate'
    assert evaluate.query_parameters() == {}
    assert evaluate.body_parameters() == {
        'variables': {'aVar': {'value': 'aVal', 'type': 'aType', 'valueInfo': 'anInfo'}}
    }


def test_evaluate_path(engine_url):
    evaluate_id = pycamunda.decisiondef.Evaluate(
        url=engine_url, id_='anId'
    )
    evaluate_key = pycamunda.decisiondef.Evaluate(
        url=engine_url, key='aKey'
    )
    evaluate_tenant = pycamunda.decisiondef.Evaluate(
        url=engine_url, key='aKey', tenant_id='aTenantId'
    )

    assert evaluate_id.url == engine_url + '/decision-definition/anId/evaluate'
    assert evaluate_key.url == engine_url + '/decision-definition/key/aKey/evaluate'
    assert evaluate_tenant.url == engine_url + '/decision-definition/key/aKey' \
                                               '/tenant-id/aTenantId/evaluate'


@unittest.mock.patch('requests.Session.request')
def test_evaluate_calls_requests(mock, engine_url):
    evaluate = pycamunda.decisiondef.Evaluate(url=engine_url, id_='anId')
    evaluate()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_evaluate_raises_pycamunda_exception(engine_url):
    evaluate = pycamunda.decisiondef.Evaluate(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        evaluate()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_evaluate_raises_for_status(mock, engine_url):
    evaluate = pycamunda.decisiondef.Evaluate(url=engine_url, id_='anId')
    try:
        evaluate()
    except AttributeError:
        pass

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_evaluate_returns_tuple(engine_url):
    evaluate = pycamunda.decisiondef.Evaluate(url=engine_url, id_='anId')
    result = evaluate()

    assert isinstance(result, tuple)
