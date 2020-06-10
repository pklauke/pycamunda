# -*- coding: utf-8 -*-

"""This module provides access to the deployment REST api of Camunda."""

from __future__ import annotations
import datetime as dt
import dataclasses
import typing

import requests

import pycamunda.variable
import pycamunda.base
from pycamunda.request import QueryParameter, PathParameter, BodyParameter

URL_SUFFIX = '/deployment'


@dataclasses.dataclass
class Deployment:
    """Data class of deployment as returned by the REST api of Camunda."""
    id_: str
    name: str
    source: str
    tenant_id: str
    deployment_time: dt.datetime = None

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> Deployment:
        deployment = cls(
            id_=data['id'],
            name=data['name'],
            source=data['source'],
            tenant_id=data['tenantId'],
        )
        if data['deploymentTime'] is not None:
            deployment.deployment_time = pycamunda.base.from_isoformat(data['deploymentTime'])

        return deployment


@dataclasses.dataclass
class Resource:
    """Data class of resource as returned by the REST api of Camunda."""
    id_: str
    name: str
    deployment_id: str

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> Resource:
        return cls(
            id_=data['id'],
            name=data['name'],
            deployment_id=data['deploymentId']
        )


class GetList(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('id')
    name = QueryParameter('name')
    name_like = QueryParameter('nameLike')
    source = QueryParameter('source')
    without_source = QueryParameter('withoutSource')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    include_deployments_without_tenant_id = QueryParameter(
        'includeDeploymentsWithoutTenantId', provide=pycamunda.base.value_is_true
    )
    after = QueryParameter('after')
    before = QueryParameter('before')
    sort_by = QueryParameter(
        'sortBy',
        mapping={
            'id_': 'id',
            'name': 'name',
            'definition_time': 'definitionTime',
            'tenant_id': 'tenantId',
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
        name: str = None,
        name_like: str = None,
        source: str = None,
        without_source: bool = None,
        tenant_id_in: typing.Iterable[str] = None,
        without_tenant_id: bool = False,
        include_deployments_without_tenant_id: bool = False,
        after: dt.datetime = None,
        before: dt.datetime = None,
        sort_by: str = None,
        ascending: bool = True,
        first_result: int = None,
        max_results: int = None,
    ):
        """Get a list of deployments.
        
        :param url: Camunda Rest engine URL.
        :param id_: Filter by id.
        :param name: Filter by name.
        :param name_like: Filter by a substring of the name.
        :param source: Filter by deployment source.
        :param without_source: Filter deployments without source.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Whether to include only deployments that belong to no tenant.
        :param include_deployments_without_tenant_id: Whether to include deployments that belong to
                                                      no tenant.
        :param after: Filter by the deployment date after the provided data.
        :param before: Filter by the deployment date before the provided data.
        :param sort_by: Sort the results by 'id', 'name', 'deployment_time' or 'tenant_id'.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.id_ = id_
        self.name = name
        self.name_like = name_like
        self.source = source
        self.without_source = without_source
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.include_deployments_without_tenant_id = include_deployments_without_tenant_id
        self.after = after
        self.before = before
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results

    def __call__(self, *args, **kwargs) -> typing.Tuple[Deployment]:
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return tuple(Deployment.load(deployment_json) for deployment_json in response.json())


class Get(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get a deployment.

        :param url: Camunda Rest engine url.
        :param id_: Id of the deployment.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> Deployment:
        """Send the request."""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return Deployment.load(response.json())


class Create(pycamunda.base.CamundaRequest):

    name = BodyParameter('deployment-name')
    enable_duplicate_filtering = BodyParameter('enable-duplicate-filtering')
    deploy_changed_only = BodyParameter('deploy-changed-only')
    source = BodyParameter('deployment-source')
    tenant_id = BodyParameter('tenant-id')

    def __init__(
        self,
        url: str,
        name: str,
        source: str = None,
        enable_duplicate_filtering: bool = False,
        deploy_changed_only: bool = False,
        tenant_id: str = None
    ):
        """Create a deployment with one or multiple resources (e.g. bpmn diagrams).

        :param url: Camunda Rest engine url
        :param name: Name of the deployment.
        :param source: Source of the deployment.
        :param enable_duplicate_filtering: Whether to check if a deployment with the same name
                                           already exists. If one does, no new deployment is done.
        :param deploy_changed_only: Whether to check if already deployed resources that are also
                                    contained in this deployment have changed. The ones that do not
                                    will not created again.
        :param tenant_id: Id of the tenant to create the deployment for.
        """
        super().__init__(url=url + URL_SUFFIX + '/create')
        self.name = name
        self.source = source
        self.enable_duplicate_filtering = enable_duplicate_filtering
        self.deploy_changed_only = deploy_changed_only
        self.tenant_id = tenant_id

        self.files = []

    def add_resource(self, file) -> None:
        """Add a resource to the deployment.

        :param file: Binary data of the resource.
        """
        self.files.append(file)

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        assert bool(self.files), 'Cannot create deployment without resources.'
        params = self.body_parameters()
        try:
            response = requests.post(
                self.url,
                data=params,
                files={f'resource-{i}': resource for i, resource in enumerate(self.files)}
            )
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)


class GetResources(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get the resources of a deployment.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the the deployment.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/resources')
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> typing.Tuple[Resource]:
        """Send the request."""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return tuple(Resource.load(resource_json) for resource_json in response.json())


class GetResource(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    resource_id = PathParameter('resourceId')

    def __init__(self, url: str, id_: str, resource_id: str, binary: bool = False):
        """Get a resource of a deployment.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the the deployment.
        :param resource_id: Id of the resource.
        :param binary: Whether to request binary content of the resource.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/resources/{resourceId}')
        self.id_ = id_
        self.resource_id = resource_id
        self.binary = binary

    @property
    def url(self):
        return super().url + ('/data' if self.binary else '')

    def __call__(self, *args, **kwargs) -> typing.Union[Resource, typing.ByteString]:
        """Send the request."""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        if self.binary:
            return response.content
        return Resource.load(response.json())


class Delete(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    cascade = QueryParameter('cascade')
    skip_custom_listeners = QueryParameter('skipCustomListeners')
    skip_io_mappings = QueryParameter('skipIoMappings')

    def __init__(
        self,
        url: str,
        id_: str,
        cascade: bool = False,
        skip_custom_listeners: bool = False,
        skip_io_mappings: bool = False
    ):
        """Delete a deployment.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the the deployment.
        :param cascade: Whether to cascade the action to all process instances (including historic).
        :param skip_custom_listeners: Whether to skip custom listeners and notify only builtin ones.
        :param skip_io_mappings: Whether to skip input/output mappings.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.cascade = cascade
        self.skip_custom_listeners = skip_custom_listeners
        self.skip_io_mappings = skip_io_mappings

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        try:
            response = requests.delete(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)
