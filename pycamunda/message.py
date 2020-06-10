# -*- coding: utf-8 -*-

"""This module provides access to the message REST api of Camunda."""

from __future__ import annotations
import dataclasses
import enum
import typing

import requests

import pycamunda.processinst
import pycamunda.execution
import pycamunda.variable
import pycamunda.base
from pycamunda.request import BodyParameter

URL_SUFFIX = '/message'


class ResultType(enum.Enum):
    process_definition = 'ProcessDefinition'
    execution = 'Execution'


@dataclasses.dataclass
class MessageCorrelationResult:
    """Data class of message correlation result as returned by the REST api of Camunda."""
    result_type: ResultType
    process_instance: pycamunda.processinst.ProcessInstance = None
    execution: pycamunda.execution.Execution = None
    variables: typing.Tuple[pycamunda.variable.Variable] = None

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> MessageCorrelationResult:

        message_result = cls(result_type=ResultType(data['resultType']))

        if message_result.result_type == ResultType.process_definition:
            message_result.process_instance = pycamunda.processinst.ProcessInstance.load(
                data['processInstance']
            )
        elif message_result.result_type == ResultType.execution:
            message_result.execution = pycamunda.execution.Execution.load(data['execution'])

        try:
            variables = data['variables']
        except KeyError:
            pass
        else:
            message_result.variables = tuple(
                pycamunda.variable.Variable.load(variable_json) for variable_json in variables
            )

        return message_result


class _Correlate(pycamunda.base.CamundaRequest):

    message_name = BodyParameter('messageName')
    business_key = BodyParameter('businessKey')
    tenant_id = BodyParameter('tenantId')
    without_tenant_id = BodyParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    process_instance_id = BodyParameter('processInstanceId')
    correlation_keys = BodyParameter('correlationKeys')
    local_correlation_keys = BodyParameter('localCorrelationKeys')
    process_variables = BodyParameter('processVariables')
    process_variables_local = BodyParameter('processVariablesLocal')
    all_ = BodyParameter('all')
    result_enabled = BodyParameter('resultEnabled')
    variables_in_result_enabled = BodyParameter('variablesInResultEnabled')

    def __init__(
        self,
        url: str,
        message_name: str,
        all_: bool,
        business_key: str = None,
        tenant_id: str = None,
        without_tenant_id: bool = False,
        process_instance_id: str = None,
        result_enabled: bool = False,
        variables_in_result_enabled: bool = False
    ):
        """Correlate a message to one or multiple entities. Entities are executions and process
        definitions.

        :param url: Camunda Rest engine URL.
        :param message_name: Name of the message to correlate.
        :param all_: Whether to correlate the message to all or just one entity.
        :param business_key: Correlate only to executions that belong to a process instance with the
                             provided business key.
        :param tenant_id: Correlate only to entities which belong to the provided tenant.
        :param without_tenant_id: Whether to correlate only to entities that belong to no tenant.
        :param process_instance_id: Correlate only to a specific process instance.
        :param result_enabled: Whether to return message correlation results.
        :param variables_in_result_enabled: Whether the returned message correlation results contain
                                            process instance variables.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.message_name = message_name
        self.all_ = all_
        self.business_key = business_key
        self.tenant_id = tenant_id
        self.without_tenant_id = without_tenant_id
        self.process_instance_id = process_instance_id
        self.result_enabled = result_enabled
        self.variables_in_result_enabled = variables_in_result_enabled

        self.correlation_keys = {}
        self.local_correlation_keys = {}
        self.process_variables = {}
        self.process_variables_local = {}

    def add_correlation_key(self, name: str, value: typing.Any, type_: str = None) -> None:
        """Add a correlation key. Used for correlation of process instances that wait for incoming
        messages. Only global process instance variables are considered.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Type of the variable.
        """
        self.correlation_keys[name] = {'value': value, 'type': type_}

    def add_local_correlation_key(self, name: str, value: typing.Any, type_: str = None) -> None:
        """Add a correlation key. Used for correlation of process instances that wait for incoming
        messages. Only variables in the execution scope are considered.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Type of the variable.
        """
        self.local_correlation_keys[name] = {'value': value, 'type': type_}

    def add_process_variable(
        self,
        name: str,
        value: typing.Any,
        type_: str = None,
        value_info: typing.Mapping = None
    ) -> None:
        """Add variables to the process after correlating the message.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable.
        :param value_info: Additional information regarding the value type.
        """
        self.process_variables[name] = {'value': value, 'type': type_, 'valueInfo': value_info}

    def add_local_process_variable(
        self,
        name: str,
        value: typing.Any,
        type_: str = None,
        value_info: typing.Mapping = None
    ) -> None:
        """Add local variables to the process after correlating the message.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable.
        :param value_info: Additional information regarding the value type.
        """
        self.process_variables_local[name] = {
            'value': value, 'type': type_, 'valueInfo': value_info
        }

    def __call__(self, *args, **kwargs) -> typing.Tuple[MessageCorrelationResult]:
        """Send the request."""
        params = self.body_parameters()
        try:
            response = requests.post(self.url, json=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return tuple(
            MessageCorrelationResult.load(data=result_json) for result_json in response.json()
        )


class CorrelateSingle(_Correlate):

    def __init__(
        self,
        url: str,
        message_name: str,
        business_key: str = None,
        tenant_id: str = None,
        without_tenant_id: bool = False,
        process_instance_id: str = None,
        result_enabled: bool = False,
        variables_in_result_enabled: bool = False
    ):
        """Correlate a message to one or multiple entities. Entities are executions and process
        definitions.

        :param url: Camunda Rest engine URL.
        :param message_name: Name of the message to correlate.
        :param all_: Whether to correlate the message to all or just one entity.
        :param business_key: Correlate only to executions that belong to a process instance with the
                             provided business key.
        :param tenant_id: Correlate only to entities which belong to the provided tenant.
        :param without_tenant_id: Whether to correlate only to entities that belong to no tenant.
        :param process_instance_id: Correlate only to a specific process instance.
        :param result_enabled: Whether to return message correlation results.
        :param variables_in_result_enabled: Whether the returned message correlation results contain
                                            process instance variables.
        """
        super().__init__(
            url=url,
            message_name=message_name,
            all_=False,
            business_key=business_key,
            tenant_id=tenant_id,
            without_tenant_id=without_tenant_id,
            process_instance_id=process_instance_id,
            result_enabled=result_enabled,
            variables_in_result_enabled=variables_in_result_enabled
        )


class CorrelateAll(_Correlate):

    def __init__(
        self,
        url: str,
        message_name: str,
        business_key: str = None,
        tenant_id: str = None,
        without_tenant_id: bool = False,
        process_instance_id: str = None,
        result_enabled: bool = False,
        variables_in_result_enabled: bool = False
    ):
        """Correlate a message to one or multiple entities. Entities are executions and process
        definitions.

        :param url: Camunda Rest engine URL.
        :param message_name: Name of the message to correlate.
        :param all_: Whether to correlate the message to all or just one entity.
        :param business_key: Correlate only to executions that belong to a process instance with the
                             provided business key.
        :param tenant_id: Correlate only to entities which belong to the provided tenant.
        :param without_tenant_id: Whether to correlate only to entities that belong to no tenant.
        :param process_instance_id: Correlate only to a specific process instance.
        :param result_enabled: Whether to return message correlation results.
        :param variables_in_result_enabled: Whether the returned message correlation results contain
                                            process instance variables.
        """
        super().__init__(
            url=url,
            message_name=message_name,
            all_=True,
            business_key=business_key,
            tenant_id=tenant_id,
            without_tenant_id=without_tenant_id,
            process_instance_id=process_instance_id,
            result_enabled=result_enabled,
            variables_in_result_enabled=variables_in_result_enabled
        )
