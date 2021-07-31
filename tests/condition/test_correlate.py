# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.condition
import pycamunda.processinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, response_mock


def test_evaluate_params(engine_url, evaluate_input, evaluate_output):
    evaluate = pycamunda.condition.Evaluate(url=engine_url, **evaluate_input)

    assert evaluate.url == engine_url + '/condition'
    assert evaluate.query_parameters() == {}
    assert evaluate.body_parameters() == {**evaluate_output}


def test_evaluate_method_params(engine_url):
    evaluate = pycamunda.condition.Evaluate(url=engine_url)
    evaluate.add_variable(name='aName', value='aValue', type_='String', value_info={})
    assert evaluate.body_parameters()['variables'] == {
        'aName': {'value': 'aValue', 'type': 'String', 'valueInfo': {}}
    }


@unittest.mock.patch('pycamunda.processinst.ProcessInstance', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_evaluate_calls_requests(mock, engine_url):
    evaluate = pycamunda.condition.Evaluate(url=engine_url)
    evaluate()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_evaluate_raises_pycamunda_exception(engine_url):
    evaluate = pycamunda.condition.Evaluate(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        evaluate()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.processinst.ProcessInstance', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_correlatesingle_raises_for_status(mock, engine_url):
    evaluate = pycamunda.condition.Evaluate(url=engine_url)
    evaluate()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_evaluate_returns_processinstance(engine_url):
    evaluate = pycamunda.condition.Evaluate(url=engine_url)
    results = evaluate()

    assert isinstance(results, tuple)
    assert all(isinstance(result, pycamunda.processinst.ProcessInstance) for result in results)
