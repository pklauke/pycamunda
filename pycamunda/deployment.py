# -*- coding: utf-8 -*-

"""This module provides access to the deployment REST api of Camunda."""

from __future__ import annotations
import datetime
import dataclasses
import typing

import requests

import pycamunda.variable
import pycamunda.request
from pycamunda.request import PathParameter, QueryParameter, BodyParameter


URL_SUFFIX = "/deployment"


@dataclasses.dataclass
class Deployment:
    id_: str
    name: str
    source: str
    tenant_id: str
    deployment_time: datetime.datetime

    @classmethod
    def load(cls, data):
        return cls(
            id_=data["id"],
            name=data["name"],
            source=data["source"],
            tenant_id=data["tenantId"],
            deployment_time=data["deploymentTime"],
        )


class GetList(pycamunda.request.CamundaRequest):

    id_ = QueryParameter("id")
    name = QueryParameter("name")
    name_like = QueryParameter("nameLike")
    source = QueryParameter("source")
    without_source = QueryParameter("withoutSource")
    tenant_id_in = QueryParameter("tenantIdIn")
    without_tenant_id = QueryParameter("withoutTenantId", provide=pycamunda.request.value_is_true)
    include_deployments_without_tenant_id = QueryParameter(
        "includeDeploymentsWithoutTenantId", provide=pycamunda.request.value_is_true
    )
    after = QueryParameter("after")
    before = QueryParameter("before")
    sort_by = QueryParameter(
        "sortBy",
        mapping={
            "id_": "id",
            "name": "name",
            "definition_time": "definitionTime",
            "tenant_id": "tenantId",
        },
    )
    ascending = QueryParameter(
        "sortOrder",
        mapping={True: "asc", False: "desc"},
        provide=lambda self, obj, obj_type: "sort_by" in vars(self),
    )
    first_result = QueryParameter("firstResult")
    max_results = QueryParameter("maxResults")

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
        after: datetime.datetime = None,
        before: datetime.datetime = None,
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
        super().__init__(url + URL_SUFFIX)
        self.id_ = id_
        self.name = name
        self.name_like = name_like
        self.source = source
        self.without_source = without_source
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.include_deployments_without_tenant_id = include_deployments_without_tenant_id
        if after is not None:
            self.after = pycamunda.variable.isoformat(after)
        if before is not None:
            self.before = pycamunda.variable.isoformat(before)
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results

    def send(self) -> typing.Tuple[Deployment]:
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return tuple(Deployment.load(deployment_json) for deployment_json in response.json())
