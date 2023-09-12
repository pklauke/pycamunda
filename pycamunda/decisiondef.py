# -*- coding: utf-8 -*-

"""This module provides access to the decision definition REST api of Camunda."""

from __future__ import annotations
import typing
import dataclasses

import pycamunda.variable
import pycamunda.base
from pycamunda.request import QueryParameter, PathParameter, BodyParameter


URL_SUFFIX = '/decision-definition'


__all__ = ['GetList', 'Count', 'Get', 'GetXML', 'GetDiagram', 'Evaluate']


@dataclasses.dataclass
class DecisionDefinition:
    """Data class of decision definition as returned by the REST api of Camunda."""
    id_: str
    key: str
    category: str
    name: str
    version: int
    resource: str
    deployment_id: str
    decision_requirements_definition_id: str
    decision_requirements_definition_key: str
    tenant_id: str
    version_tag: str
    history_time_to_live: int

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> DecisionDefinition:
        return cls(
            id_=data['id'],
            key=data['key'],
            category=data['category'],
            name=data['name'],
            version=data['version'],
            resource=data['resource'],
            deployment_id=data['deploymentId'],
            decision_requirements_definition_id=data['decisionRequirementsDefinitionId'],
            decision_requirements_definition_key=data['decisionRequirementsDefinitionKey'],
            tenant_id=data['tenantId'],
            version_tag=data['versionTag'],
            history_time_to_live=data['historyTimeToLive']
        )


class GetList(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('decisionDefinitionId')
    id_in = QueryParameter('decisionDefinitionIdIn')
    name = QueryParameter('name')
    name_like = QueryParameter('nameLike')
    deployment_id = QueryParameter('deploymentId')
    key = QueryParameter('key')
    key_like = QueryParameter('keyLike')
    category = QueryParameter('category')
    category_like = QueryParameter('categoryLike')
    version = QueryParameter('version')
    latest_version = QueryParameter('latestVersion', provide=pycamunda.base.value_is_true)
    resource_name = QueryParameter('resourceName')
    resource_name_like = QueryParameter('resourceNameLike')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    include_without_tenant_id = QueryParameter(
        'includeDecisionDefinitionsWithoutTenantId',
        provide=pycamunda.base.value_is_true
    )
    sort_by = QueryParameter(
        'sortBy',
        mapping={
            'category': 'category',
            'key': 'key',
            'id_': 'id',
            'name': 'name',
            'version': 'version',
            'deployment_id': 'deploymentId',
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
        id_: str = None,
        id_in: typing.Iterable[str] = None,
        name: str = None,
        name_like: str = None,
        deployment_id: str = None,
        key: str = None,
        key_like: str = None,
        category: str = None,
        category_like: str = None,
        version: str = None,
        latest_version: bool = False,
        resource_name: str = None,
        resource_name_like: str = None,
        tenant_id_in: typing.Iterable[str] = None,
        without_tenant_id: bool = False,
        include_without_tenant_id: bool = False,
        sort_by: str = None,
        ascending: bool = True,
        first_result: int = None,
        max_results: int = None,
        timeout: int = 5
    ):
        """Query for a list of decision definitions using a list of parameters. The size of the
        result set can be retrieved by using the Count method.

        :param url: Camunda Rest engine URL.
        :param id_: Filter by id.
        :param id_in: Filter whether the id is one of multiple ones.
        :param name: Filter by name.
        :param name_like: Filter by a substring of the name.
        :param deployment_id: Filter by deployment id.
        :param key: Key of the process definition.
        :param key_like: Filter by a substring of the key.
        :param category: Filter by category.
        :param category_like: Filter by a substring of the category.
        :param version: Filter by version.
        :param latest_version: Whether to include only the latest versions.
        :param resource_name: Filter by resource name.
        :param resource_name_like: Filter by a substring of the resource name.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Whether to include only decision definitions that belong to no
                                  tenant.
        :param include_without_tenant_id: Whether to include decision definitions that belong to no
                                          tenant.
        :param sort_by: Sort the results by 'category', 'key', 'id_', 'name', 'version',
                        'deployment_id' or 'tenant_id'. Sorting by 'version_tag' is string-based.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.id_ = id_
        self.id_in = id_in
        self.name = name
        self.name_like = name_like
        self.deployment_id = deployment_id
        self.key = key
        self.key_like = key_like
        self.category = category
        self.category_like = category_like
        self.version = version
        self.latest_version = latest_version
        self.resource_name = resource_name
        self.resource_name_like = resource_name_like
        self.incident_type = None
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.include_without_tenant_id = include_without_tenant_id
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> typing.Tuple[DecisionDefinition]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return tuple(
            DecisionDefinition.load(decisiondef_json) for decisiondef_json in response.json()
        )


class Count(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('decisionDefinitionId')
    id_in = QueryParameter('decisionDefinitionIdIn')
    name = QueryParameter('name')
    name_like = QueryParameter('nameLike')
    deployment_id = QueryParameter('deploymentId')
    key = QueryParameter('key')
    key_like = QueryParameter('keyLike')
    category = QueryParameter('category')
    category_like = QueryParameter('categoryLike')
    version = QueryParameter('version')
    latest_version = QueryParameter('latestVersion', provide=pycamunda.base.value_is_true)
    resource_name = QueryParameter('resourceName')
    resource_name_like = QueryParameter('resourceNameLike')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    include_without_tenant_id = QueryParameter(
        'includeDecisionDefinitionsWithoutTenantId',
        provide=pycamunda.base.value_is_true
    )

    def __init__(
        self,
        url: str,
        id_: str = None,
        id_in: typing.Iterable[str] = None,
        name: str = None,
        name_like: str = None,
        deployment_id: str = None,
        key: str = None,
        key_like: str = None,
        category: str = None,
        category_like: str = None,
        version: str = None,
        latest_version: bool = False,
        resource_name: str = None,
        resource_name_like: str = None,
        tenant_id_in: typing.Iterable[str] = None,
        without_tenant_id: bool = False,
        include_without_tenant_id: bool = False,
        timeout: int = 5
    ):
        """Count decision definitions.

        :param url: Camunda Rest engine URL.
        :param id_: Filter by id.
        :param id_in: Filter whether the id is one of multiple ones.
        :param name: Filter by name.
        :param name_like: Filter by a substring of the name.
        :param deployment_id: Filter by deployment id.
        :param key: Key of the process definition.
        :param key_like: Filter by a substring of the key.
        :param category: Filter by category.
        :param category_like: Filter by a substring of the category.
        :param version: Filter by version.
        :param latest_version: Whether to include only the latest versions.
        :param resource_name: Filter by resource name.
        :param resource_name_like: Filter by a substring of the resource name.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Whether to include only decision definitions that belong to no
                                  tenant.
        :param include_without_tenant_id: Whether to include decision definitions that belong to no
                                          tenant.
        """
        super().__init__(url=url + URL_SUFFIX + '/count')
        self.id_ = id_
        self.id_in = id_in
        self.name = name
        self.name_like = name_like
        self.deployment_id = deployment_id
        self.key = key
        self.key_like = key_like
        self.category = category
        self.category_like = category_like
        self.version = version
        self.latest_version = latest_version
        self.resource_name = resource_name
        self.resource_name_like = resource_name_like
        self.incident_type = None
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.include_without_tenant_id = include_without_tenant_id
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> typing.Tuple[DecisionDefinition]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return response.json()['count']


class Get(pycamunda.base._PathMixin, pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')

    def __init__(self, url: str, id_: str = None, key: str = None, tenant_id: str = None, timeout: int = 5):
        """Get a decision definition.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the decision definition.
        :param key: Key of the decision definition.
        :param tenant_id: Id of the tenant the decision definition belongs to.

        """
        super().__init__(url=url + URL_SUFFIX + '/{path}')
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> DecisionDefinition:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return DecisionDefinition.load(response.json())


class GetXML(pycamunda.base._PathMixin, pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')

    def __init__(
        self,
        url: str,
        id_: str = None,
        key: str = None,
        tenant_id: str = None,
        timeout: int = 5
    ):
        """Retrieve the CMMN XML of a decision definition.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the decision definition.
        :param key: Key of the decision definition.
        :param tenant_id: Id of the tenant the decision definition belongs to.
        """
        super().__init__(url=url + URL_SUFFIX + '/{path}/xml')
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> str:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return response.json()['dmnXml']


class GetDiagram(pycamunda.base._PathMixin, pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')

    def __init__(self, url: str, id_: str = None, key: str = None, tenant_id: str = None, timeout: int = 5):
        """Get the diagram of a decision definition.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the decision definition.
        :param key: Key of the decision definition.
        """
        super().__init__(url=url + URL_SUFFIX + '/{path}/diagram')
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id
        self.timeout = timeout

    def __call__(self, *args, **kwargs):
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return response.content


class Evaluate(pycamunda.base._PathMixin, pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')

    variables = BodyParameter('variables')

    def __init__(self, url: str, id_: str = None, key: str = None, tenant_id: str = None, timeout: int = 5):
        """Evaluate the result of a decision definition.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the decision definition.
        :param key: Key of the decision definition.
        :param tenant_id: Id of the tenant the decision definition belongs to.
        """
        super().__init__(url=url + URL_SUFFIX + '/{path}/evaluate')
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id

        self.variables = {}
        self.timeout = timeout

    def add_variable(
        self, name: str, value: typing.Any, type_: str = None, value_info: str = None
    ) -> None:
        """Add a variable for the evaluation of the decision definition.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable.
        :param value_info: Additional information regarding the value type.
        """
        self.variables[name] = {'value': value, 'type': type_, 'valueInfo': value_info}

    def __call__(self, *args, **kwargs) -> typing.Tuple[typing.Dict]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)

        return tuple(
            {
                name: pycamunda.variable.Variable.load(var_json)
                for name, var_json in rule.items()
            }
            for rule in response.json()
        )
