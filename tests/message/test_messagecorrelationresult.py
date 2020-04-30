# -*- coding: utf-8 -*-

import pytest

import pycamunda.message
import pycamunda.processinst
import pycamunda.execution
import pycamunda.variable


def test_messagecorrelationresult_load_definition(my_process_instance_json):
    result_json = {
        'resultType': 'ProcessDefinition',
        'processInstance': my_process_instance_json,
        'variables': [{'name': 'aVar', 'value': 'aVal', 'type': None, 'valueInfo': {}}]
    }
    correlation_result = pycamunda.message.MessageCorrelationResult.load(result_json)

    assert correlation_result.result_type.value == result_json['resultType']
    assert correlation_result.process_instance == pycamunda.processinst.ProcessInstance.load(
        result_json['processInstance']
    )
    assert isinstance(correlation_result.variables, tuple)


def test_messagecorrelationresult_load_execution(my_execution_json):
    result_json = {
        'resultType': 'Execution',
        'execution': my_execution_json,
        'variables': [{'name': 'aVar', 'value': 'aVal', 'type': None, 'valueInfo': {}}]
    }
    correlation_result = pycamunda.message.MessageCorrelationResult.load(result_json)

    assert correlation_result.result_type.value == result_json['resultType']
    assert correlation_result.execution == pycamunda.execution.Execution.load(
        result_json['execution']
    )
    assert isinstance(correlation_result.variables, tuple)


def test_messagecorrelationresult_load_raises_keyerror():
    with pytest.raises(KeyError):
        pycamunda.message.MessageCorrelationResult.load(data={})
