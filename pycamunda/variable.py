# -*- coding: utf-8 -*-

"""This module provides access to the variable instance REST api of Camunda"""

from __future__ import annotations
import dataclasses
import typing

import requests

import pycamunda.base
from pycamunda.request import QueryParameter, PathParameter

URL_SUFFIX = '/variable-instance'


@dataclasses.dataclass
class Variable:
    """Data class of variable as returned by the REST api of Camunda."""
    value: typing.Any
    type_: str
    value_info: typing.Dict
    local: bool = None

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> Variable:
        variable = cls(
            value=data['value'],
            type_=data['type'],
            value_info=data['valueInfo']
        )
        try:
            variable.local = data['local']
        except KeyError:
            pass
        return variable


@dataclasses.dataclass
class VariableInstance:
    """Data class of variable instance as returned by the REST api of Camunda."""
    id_: str
    name: str
    type_: str
    value: typing.Any
    value_info: typing.Dict
    process_instance_id: str
    execution_id: str
    case_instance_id: str
    case_execution_id: str
    task_id: str
    activity_instance_id: str
    tenant_id: str
    error_message: str

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> VariableInstance:
        return cls(
            id_=data['id'],
            name=data['name'],
            type_=data['type'],
            value=data['value'],
            value_info=data['valueInfo'],
            process_instance_id=data['processInstanceId'],
            execution_id=data['executionId'],
            case_instance_id=data['caseInstanceId'],
            case_execution_id=data['caseExecutionId'],
            task_id=data['taskId'],
            activity_instance_id=data['activityInstanceId'],
            tenant_id=data['tenantId'],
            error_message=data['errorMessage']
        )


class GetList(pycamunda.base.CamundaRequest):

    name = QueryParameter('variableName')
    name_like = QueryParameter('variableNameLike')
    process_instance_id_in = QueryParameter('processInstanceId')
    execution_id_in = QueryParameter('executionIdIn')
    case_instance_id_in = QueryParameter('caseInstanceIdIn')
    case_execution_id_in = QueryParameter('caseExecutionIdIn')
    task_id_in = QueryParameter('taskIdIn')
    activity_instance_id_in = QueryParameter('activityInstanceIdIn')
    tenant_id_in = QueryParameter('tenantIdIn')
    variable_values = QueryParameter('variableValues')
    sort_by = QueryParameter(
        'sortBy',
        mapping={
            'name': 'variableName',
            'type_': 'variableType',
            'activity_instance_id': 'activityInstanceIdIn',
            'tenant_id': 'tenantId'
        }
    )
    ascending = QueryParameter(
        'sortOrder',
        mapping={True: 'asc', False: 'desc'},
        provide=lambda self, obj, obj_type: vars(obj).get('sort_by', None) is not None
    )
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')
    deserialize_values = QueryParameter('deserializeValues')

    def __init__(
        self,
        url: str,
        name: str = None,
        name_like: str = None,
        process_instance_id_in: typing.Iterable[str] = None,
        case_instance_id_in: typing.Iterable[str] = None,
        case_execution_id_in: typing.Iterable[str] = None,
        task_id_in: typing.Iterable[str] = None,
        activity_instance_id_in: typing.Iterable[str] = None,
        tenant_id_in: typing.Iterable[str] = None,
        sort_by: str = None,
        ascending: bool = True,
        first_result: int = None,
        max_results: int = None,
        deserialize_values: bool = False
    ):
        """Get a list of variable instances.

        :param url: Camunda Rest engine URL.
        :param name: Filter by variable name.
        :param name_like: Filter by a substring of the variable name.
        :param process_instance_id_in: Filter whether the process instance id is one of multiple
                                       ones.
        :param case_instance_id_in: Filter whether the case instance id is one of multiple ones.
        :param case_execution_id_in: Filter whether the case execution id is one of multiple ones.
        :param task_id_in: Filter whether the task id is one of multiple ones.
        :param activity_instance_id_in: Filter whether the activity instance id is one of multiple
                                        ones.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param sort_by: Sort the results by 'name', 'type_', 'activity_instance_id' or 'tenant_id'.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        :param deserialize_values: Whether serializable variable values are deserialized on server
                                   side.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.name = name
        self.name_like = name_like
        self.process_instance_id_in = process_instance_id_in
        self.case_instance_id_in = case_instance_id_in
        self.case_execution_id_in = case_execution_id_in
        self.task_id_in = task_id_in
        self.activity_instance_id_in = activity_instance_id_in
        self.tenant_id_in = tenant_id_in
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results
        self.deserialize_values = deserialize_values

        self.variable_values = []

    def _add_value_filter(self, name: str, criteria: str, value: str) -> None:
        """Add a filter to include only variables with certain values.

        :param name: Name of the variable.
        :param criteria: Filter criteria. Valid values are 'eq' for equal, 'neq' for not equal,
                         'gt' for greater than, 'gteq' for greater than or equal, 'lt' for less
                         than, 'lteq' for less than or equal and 'like'.
        :param value: Value to filter for.
        """
        self.variable_values.append((name, criteria, str(value)))

    def add_equal_value_filter(self, name: str, value: typing.Any) -> None:
        """Add a filter to include only variables with values equal a provided value.

        :param name: Name of the variable.
        :param value: Value to filter for.
        """
        self._add_value_filter(name=name, criteria='eq', value=value)

    def add_not_equal_value_filter(self, name: str, value: typing.Any) -> None:
        """Add a filter to include only variables with values not equal a provided value.

        :param name: Name of the variable.
        :param value: Value to filter for.
        """
        self._add_value_filter(name=name, criteria='neq', value=value)

    def add_greater_than_value_filter(self, name: str, value: typing.Any) -> None:
        """Add a filter to include only variables with values greater than a provided value.

        :param name: Name of the variable.
        :param value: Value to filter for.
        """
        self._add_value_filter(name=name, criteria='gt', value=value)

    def add_greater_than_equal_value_filter(self, name: str, value: typing.Any) -> None:
        """Add a filter to include only variables with values greater than or equal a provided
        value.

        :param name: Name of the variable.
        :param value: Value to filter for.
        """
        self._add_value_filter(name=name, criteria='gteq', value=value)

    def add_less_than_value_filter(self, name: str, value: typing.Any) -> None:
        """Add a filter to include only variables with values less than a provided value.

        :param name: Name of the variable.
        :param value: Value to filter for.
        """
        self._add_value_filter(name=name, criteria='lt', value=value)

    def add_less_than_equal_value_filter(self, name: str, value: typing.Any) -> None:
        """Add a filter to include only variables with values less than or equal a provided value.

        :param name: Name of the variable.
        :param value: Value to filter for.
        """
        self._add_value_filter(name=name, criteria='lteq', value=value)

    def add_like_value_filter(self, name: str, value: typing.Any) -> None:
        """Add a filter to include only variables with values like a provided value.

        :param name: Name of the variable.
        :param value: Value to filter for.
        """
        self._add_value_filter(name=name, criteria='like', value=value)

    def query_parameters(self, apply: typing.Callable = ...):
        params = super().query_parameters(apply=apply)
        if params['variableValues']:
            params['variableValues'] = ','.join(
                ('_'.join(var_val)) for var_val in params['variableValues']
            )
        else:
            del params['variableValues']
        return params

    def __call__(self, *args, **kwargs) -> typing.Tuple[VariableInstance]:
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return tuple(VariableInstance.load(variable_json) for variable_json in response.json())


class Get(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    deserialize_value = QueryParameter('deserializeValue')

    def __init__(self, url: str, id_: str, deserialize_value: bool = False):
        """Get a variable instance.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the variable instance.
        :param deserialize_value: Whether serializable variable values are deserialized on server
                                  side.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.deserialize_value = deserialize_value

    def __call__(self, *args, **kwargs) -> VariableInstance:
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return VariableInstance.load(response.json())
