# -*- coding: utf-8 -*-

"""This module provides access to the condition REST api of Camunda."""

from __future__ import annotations
import typing

import pycamunda.processinst
import pycamunda.base
from pycamunda.request import BodyParameter

URL_SUFFIX = '/condition'


__all__ = ['Evaluate']


class Evaluate(pycamunda.base.CamundaRequest):

    variables = BodyParameter('variables')
    business_key = BodyParameter('businessKey')
    tenant_id = BodyParameter('tenantId')
    without_tenant_id = BodyParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    process_definition_id = BodyParameter('processDefinitionId')

    def __init__(
        self,
        url: str,
        business_key: str = None,
        tenant_id: str = None,
        without_tenant_id: bool = False,
        process_definition_id: str = None
    ):
        """Trigger the evaluation of conditional start events.

        :param url: Camunda Rest engine URL.
        :param business_key: Business key for the process instances that might be started.
        :param tenant_id: Tenant id of the conditions to evaluate.
        :param without_tenant_id: Whether evaluate only conditions that have no tenant.
        :param process_definition_id: Process definition id of the conditions to evaluate.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.business_key = business_key
        self.tenant_id = tenant_id
        self.without_tenant_id = without_tenant_id
        self.process_definition_id = process_definition_id

        self.variables = {}

    def add_variable(
        self,
        name: str,
        value: typing.Any,
        type_: str = None,
        value_info: typing.Mapping = None
    ) -> None:
        """Add a variable for the evaluation of the conditions.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable.
        :param value_info: Additional information regarding the value type.
        """
        self.variables[name] = {'value': value, 'type': type_, 'valueInfo': value_info}

    def __call__(self, *args, **kwargs) -> typing.Tuple[pycamunda.processinst.ProcessInstance]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)

        return tuple(
            pycamunda.processinst.ProcessInstance.load(data=result_json)
            for result_json in response.json()
        )
