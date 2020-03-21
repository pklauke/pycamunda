# -*- coding: utf-8 -*-

"""This module provides access to the process instance REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing

import requests

import pycamunda.variable
import pycamunda.request
from pycamunda.request import PathParameter, QueryParameter, BodyParameter, BodyParameterContainer


URL_SUFFIX = '/process-instance'


@dataclasses.dataclass
class ProcessInstance:
    id_: str
    definition_id: str
    business_key: str
    case_instance_id: str
    tenant_id: str
    ended: bool
    suspended: bool
    links: typing.Tuple[pycamunda.Link]
    variables: typing.Dict[str, pycamunda.variable.Variable] = None

    @classmethod
    def load(cls, data) -> ProcessInstance:
        process_instance = cls(
            id_=data['id'],
            definition_id=data['definitionId'],
            business_key=data['businessKey'],
            case_instance_id=data['caseInstanceId'],
            tenant_id=data['tenantId'],
            ended=data['ended'],
            suspended=data['suspended'],
            links=tuple(pycamunda.Link.load(link_json) for link_json in data['links']),
        )
        try:
            variables = data['variables']
        except KeyError:
            pass
        else:
            process_instance.variables = {name: pycamunda.variable.Variable.load(var_json)
                                          for name, var_json in variables.items()}

        return process_instance


class Delete(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')
    skip_custom_listeners = QueryParameter('skipCustomListeners')
    skip_io_mappings = QueryParameter('skipIoMappings')
    skip_subprocesses = QueryParameter('skipSubprocesses')
    fail_if_not_exists = QueryParameter('failIfNotExists')

    def __init__(
            self,
            url: str,
            id_: str,
            skip_custom_listeners: bool = False,
            skip_io_mappings: bool = False,
            skip_subprocesses: bool = False,
            fail_if_not_exists: bool = True
    ):
        """Delete a process instance.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process instance.
        :param skip_custom_listeners: Whether to skip custom listeners and notify only builtin ones.
        :param skip_io_mappings: Whether to skip input/output mappings.
        :param skip_subprocesses: Whether to skip subprocesses.
        :param fail_if_not_exists: Whether to fail if the provided process instance id is not found.
        """
        super().__init__(url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.skip_custom_listeners = skip_custom_listeners
        self.skip_io_mappings = skip_io_mappings
        self.skip_subprocesses = skip_subprocesses
        self.fail_if_not_exists = fail_if_not_exists

    def send(self):
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.delete(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)
