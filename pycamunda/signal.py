# -*- coding: utf-8 -*-

"""This module provides access to the signal REST api of Camunda."""

from __future__ import annotations
import typing

import requests

import pycamunda.variable
import pycamunda.base
from pycamunda.request import BodyParameter

URL_SUFFIX = '/signal'


class _Event(pycamunda.base.CamundaRequest):

    name = BodyParameter('name')
    execution_id = BodyParameter('executionId')
    variables = BodyParameter('variables')
    tenant_id = BodyParameter('tenantId')
    without_tenant_id = BodyParameter('withoutTenantId', provide=pycamunda.base.value_is_true)

    def __init__(
        self,
        url: str,
        name: str,
        execution_id: str = None,
        tenant_id: str = None,
        without_tenant_id: bool = False
    ):
        """Deliver a signal to all process definitions and executions with the specific signal
        handler.

        :param url: Camunda Rest engine URL.
        :param name: Name of the signal.
        :param execution_id: Id of the execution to deliver the signal to.
        :param tenant_id: Id of the tenant. Signal will only be delivered to process definitions or
                          executions that belong to this tenant.
        :param without_tenant_id: Whether to deliver the signal only to process definitions or
                                  executions without tenant.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.name = name
        self.execution_id = execution_id
        self.tenant_id = tenant_id
        self.without_tenant_id = without_tenant_id

        self.variables = {}

    def add_variable(
        self,
        name: str,
        value: typing.Any,
        type_: str = None,
        value_info: typing.Mapping = None
    ):
        """Add variables to the process after correlating the message.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable.
        :param value_info: Additional information regarding the value type.
        """
        self.variables[name] = {'value': value, 'type': type_, 'valueInfo': value_info}

        return self

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        params = self.body_parameters()
        try:
            response = requests.post(self.url, json=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)


class EventAll(_Event):

    def __init__(
        self,
        url: str,
        name: str,
        tenant_id: str = None,
        without_tenant_id: bool = False
    ):
        """Deliver a signal to all process definitions and executions with the specific signal
        handler.

        :param url: Camunda Rest engine URL.
        :param name: Name of the signal.
        :param tenant_id: Id of the tenant. Signal will only be delivered to process definitions or
                          executions that belong to this tenant.
        :param without_tenant_id: Whether to deliver the signal only to process definitions or
                                  executions without tenant.
        """
        super().__init__(
            url=url, name=name, tenant_id=tenant_id, without_tenant_id=without_tenant_id
        )


class EventSingle(_Event):

    def __init__(
        self,
        url: str,
        name: str,
        execution_id: str
    ):
        """Deliver a signal to all process definitions and executions with the specific signal
        handler.

        :param url: Camunda Rest engine URL.
        :param name: Name of the signal.
        :param execution_id: Id of the execution to deliver the signal to.
        """
        super().__init__(url=url, name=name, execution_id=execution_id)
