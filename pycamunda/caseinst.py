# -*- coding: utf-8 -*-

"""This module provides access to the case instance REST api of Camunda."""


from __future__ import annotations
import dataclasses
import typing

import pycamunda.base
from pycamunda.request import QueryParameter, PathParameter, BodyParameter


URL_SUFFIX = '/case-instance'


__all__ = ['GetList', 'Count', 'Get', 'Complete', 'Close', 'Terminate']


@dataclasses.dataclass
class CaseInstance:
    """Data class of case instance as returned by the REST api of Camunda."""
    id_: str
    definition_id: str
    tenant_id: str
    business_key: str
    active: bool
    completed: bool = None

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> CaseInstance:
        case_instance = cls(
            id_=data['id'],
            definition_id=data['caseDefinitionId'],
            tenant_id=data['tenantId'],
            business_key=data['businessKey'],
            active=data['active']
        )
        try:
            case_instance.completed = data['completed']
        except KeyError:
            pass

        return case_instance


class GetList(pycamunda.base.CamundaRequest):

    case_instance_id = QueryParameter('caseInstanceId')
    business_key = QueryParameter('businessKey')
    case_definition_id = QueryParameter('caseDefinitionId')
    case_definition_key = QueryParameter('caseDefinitionKey')
    deployment_id = QueryParameter('deploymentId')
    super_process_instance = QueryParameter('superProcessInstance')
    sub_process_instance = QueryParameter('subProcessInstance')
    super_case_instance = QueryParameter('superCaseInstance')
    sub_case_instance = QueryParameter('subCaseInstance')
    active = QueryParameter('active', provide=pycamunda.base.value_is_true)
    completed = QueryParameter('completed', provide=pycamunda.base.value_is_true)
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    variables = QueryParameter('variables')
    variable_names_ignore_case = QueryParameter(
        'variableNamesIgnoreCase', provide=pycamunda.base.value_is_true
    )
    variable_values_ignore_case = QueryParameter(
        'variableValuesIgnoreCase', provide=pycamunda.base.value_is_true
    )
    sort_by = QueryParameter(
        'sortBy',
        mapping={
            'case_instance_id': 'caseInstanceId',
            'case_definition_key': 'caseDefinitionKey',
            'case_definition_id': 'caseDefinitionId',
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

    def __init__(
            self,
            url: str,
            case_instance_id: str = None,
            business_key: str = None,
            case_definition_id: str = None,
            case_definition_key: str = None,
            deployment_id: str = None,
            super_process_instance: str = None,
            sub_process_instance: str = None,
            super_case_instance: str = None,
            sub_case_instance: str = None,
            active: bool = False,
            completed: bool = False,
            tenant_id_in: typing.Iterable[str] = None,
            without_tenant_id: bool = False,
            variable_names_ignore_case: bool = False,
            variable_values_ignore_case: bool = False,
            sort_by: str = None,
            ascending: bool = True,
            first_result: int = None,
            max_results: int = None
    ):
        """Get a list of case instances.

        :param url: Camunda Rest engine URL.
        :param case_instance_id: Filter by case instance id.
        :param business_key: Filter by business key.
        :param case_definition_id: Filter by case definition id.
        :param case_definition_key: Filter by case definition key.
        :param deployment_id: Filter by deployment id.
        :param super_process_instance: Filter by the id of the super process instance.
        :param sub_process_instance: Filter by the id of sub process instance.
        :param super_case_instance: Filter by the id of the super case instance.
        :param sub_case_instance: Filter by the id of sub case instance.
        :param active: Whether to include only active case instances.
        :param completed: Whether to include only complete case instances.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Whether to include only case instances that belong to no tenant.
        :param variable_names_ignore_case: Whether to match variables names case-insensitively.
        :param variable_values_ignore_case: Whether to match variables values case-insensitively.
        :param sort_by: Sort the results by 'batch_id' or 'tenant_id'.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.case_instance_id = case_instance_id
        self.business_key = business_key
        self.case_definition_id = case_definition_id
        self.case_definition_key = case_definition_key
        self.deployment_id = deployment_id
        self.super_process_instance = super_process_instance
        self.sub_process_instance = sub_process_instance
        self.super_case_instance = super_case_instance
        self.sub_case_instance = sub_case_instance
        self.active = active
        self.completed = completed
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.variable_names_ignore_case = variable_names_ignore_case
        self.variable_values_ignore_case = variable_values_ignore_case
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results

        self.variables = {}

    def add_variable(
        self, name: str, value: str, type_: str = None, value_info: typing.Mapping = None
    ) -> None:
        """Only include case instances with variables with specific values.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable.
        :param value_info: Additional information regarding the value type.
        """
        self.variables[name] = {'value': value, 'type': type_, 'valueInfo': value_info}

    def __call__(self, *args, **kwargs) -> typing.Tuple[CaseInstance]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return tuple(CaseInstance.load(batch_json) for batch_json in response.json())


class Count(pycamunda.base.CamundaRequest):

    case_instance_id = QueryParameter('caseInstanceId')
    business_key = QueryParameter('businessKey')
    case_definition_id = QueryParameter('caseDefinitionId')
    case_definition_key = QueryParameter('caseDefinitionKey')
    deployment_id = QueryParameter('deploymentId')
    super_process_instance = QueryParameter('superProcessInstance')
    sub_process_instance = QueryParameter('subProcessInstance')
    super_case_instance = QueryParameter('superCaseInstance')
    sub_case_instance = QueryParameter('subCaseInstance')
    active = QueryParameter('active', provide=pycamunda.base.value_is_true)
    completed = QueryParameter('completed', provide=pycamunda.base.value_is_true)
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    variables = QueryParameter('variables')
    variable_names_ignore_case = QueryParameter(
        'variableNamesIgnoreCase', provide=pycamunda.base.value_is_true
    )
    variable_values_ignore_case = QueryParameter(
        'variableValuesIgnoreCase', provide=pycamunda.base.value_is_true
    )

    def __init__(
            self,
            url: str,
            case_instance_id: str = None,
            business_key: str = None,
            case_definition_id: str = None,
            case_definition_key: str = None,
            deployment_id: str = None,
            super_process_instance: str = None,
            sub_process_instance: str = None,
            super_case_instance: str = None,
            sub_case_instance: str = None,
            active: bool = False,
            completed: bool = False,
            tenant_id_in: typing.Iterable[str] = None,
            without_tenant_id: bool = False,
            variable_names_ignore_case: bool = False,
            variable_values_ignore_case: bool = False
    ):
        """Count a list of case instances.

        :param url: Camunda Rest engine URL.
        :param case_instance_id: Filter by case instance id.
        :param business_key: Filter by business key.
        :param case_definition_id: Filter by case definition id.
        :param case_definition_key: Filter by case definition key.
        :param deployment_id: Filter by deployment id.
        :param super_process_instance: Filter by the id of the super process instance.
        :param sub_process_instance: Filter by the id of sub process instance.
        :param super_case_instance: Filter by the id of the super case instance.
        :param sub_case_instance: Filter by the id of sub case instance.
        :param active: Whether to include only active case instances.
        :param completed: Whether to include only complete case instances.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Whether to include only case instances that belong to no tenant.
        :param variable_names_ignore_case: Whether to match variables names case-insensitively.
        :param variable_values_ignore_case: Whether to match variables values case-insensitively.
        """
        super().__init__(url=url + URL_SUFFIX + '/count')
        self.case_instance_id = case_instance_id
        self.business_key = business_key
        self.case_definition_id = case_definition_id
        self.case_definition_key = case_definition_key
        self.deployment_id = deployment_id
        self.super_process_instance = super_process_instance
        self.sub_process_instance = sub_process_instance
        self.super_case_instance = super_case_instance
        self.sub_case_instance = sub_case_instance
        self.active = active
        self.completed = completed
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.variable_names_ignore_case = variable_names_ignore_case
        self.variable_values_ignore_case = variable_values_ignore_case

        self.variables = {}

    def add_variable(
        self, name: str, value: str, type_: str = None, value_info: typing.Mapping = None
    ) -> None:
        """Only count case instances with variables with specific values.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable.
        :param value_info: Additional information regarding the value type.
        """
        self.variables[name] = {'value': value, 'type': type_, 'valueInfo': value_info}

    def __call__(self, *args, **kwargs) -> int:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return response.json()['count']


class Get(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    case_definition_id = QueryParameter('caseDefinitionId')
    business_key = QueryParameter('businessKey')
    active = QueryParameter('active', provide=pycamunda.base.value_is_true)
    completed = QueryParameter('completed', provide=pycamunda.base.value_is_true)
    tenant_id = QueryParameter('tenantId')

    def __init__(
            self,
            url: str,
            id_: str,
            case_definition_id: str = None,
            business_key: str = None,
            active: bool = False,
            completed: bool = False,
            tenant_id: typing.Iterable[str] = None
    ):
        """Get a case instance.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the case instance.
        :param case_definition_id: Id of the case definition the case instance belongs to.
        :param business_key: The business key of the case instance.
        :param active: Whether the case instance is active.
        :param completed: Whether the case instance is completed.
        :param tenant_id: The tenant id of the case instance.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.business_key = business_key
        self.case_definition_id = case_definition_id
        self.active = active
        self.completed = completed
        self.tenant_id = tenant_id

    def __call__(self, *args, **kwargs) -> CaseInstance:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return CaseInstance.load(response.json())


class _VariableDeletionMixin(pycamunda.base.CamundaRequest):

    def body_parameters(self, apply: typing.Callable = ...) -> typing.Dict[str, typing.Any]:
        params = super().body_parameters(apply=apply)
        deletions = params.get('deletions', [])
        if isinstance(deletions, str):
            params['deletions'] = deletions.split()
        else:
            params['deletions'] = list(deletions)
        params['deletions'] = [{'name': name} for name in params['deletions']]
        return params

    def add_variable(
        self,
        name: str,
        value: str,
        type_: str = None,
        value_info: typing.Mapping = None,
        local: bool = None
    ) -> None:
        """Create or update case instance variables.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable.
        :param value_info: Additional information regarding the value type.
        :param local: Whether the creation or update will be locally and not propagated upwards.
        """
        self.variables[name] = {
            'value': value, 'type': type_, 'valueInfo': value_info,
        }
        if local is not None:
            self.variables[name]['local'] = local


class Complete(_VariableDeletionMixin, pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    variables = BodyParameter('variables')
    deletions = BodyParameter('deletions')

    def __init__(self, url: str, id_: str, deletions: typing.Iterable[str] = None):
        """Performs a transition from ACTIVE state to COMPLETED state. In addition to that,
        case instance variables can be updated and deleted.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the case instance.
        :param deletions: Variables to delete. Is executed for creating or updating variables.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/complete')
        self.id_ = id_
        self.deletions = deletions

        self.variables = {}

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)


class Close(_VariableDeletionMixin, pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    variables = BodyParameter('variables')
    deletions = BodyParameter('deletions')

    def __init__(self, url: str, id_: str, deletions: typing.Iterable[str] = None):
        """Performs a transition from COMPLETED state to CLOSED state. In addition to that,
        case instance variables can be updated and deleted.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the case instance.
        :param deletions: Variables to delete. Is executed for creating or updating variables.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/close')
        self.id_ = id_
        self.deletions = deletions

        self.variables = {}

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)


class Terminate(_VariableDeletionMixin, pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    variables = BodyParameter('variables')
    deletions = BodyParameter('deletions')

    def __init__(self, url: str, id_: str, deletions: typing.Iterable[str] = None):
        """Performs a transition from ACTIVE state to TERMINATED state. In addition to that,
        case instance variables can be updated and deleted.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the case instance.
        :param deletions: Variables to delete. Is executed for creating or updating variables.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/terminate')
        self.id_ = id_
        self.deletions = deletions

        self.variables = {}

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)
