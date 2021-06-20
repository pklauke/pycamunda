# -*- coding: utf-8 -*-

"""This module provides access to the batch REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing

import pycamunda.base
from pycamunda.request import QueryParameter, PathParameter, BodyParameter

URL_SUFFIX = '/batch'


__all__ = ['GetList', 'Count', 'Get', 'Activate', 'Suspend', 'Delete', 'GetStats', 'CountStats']


@dataclasses.dataclass
class Batch:
    """Data class of batch as returned by the REST api of Camunda."""
    id_: str
    type_: str
    total_jobs: int
    jobs_created: int
    batch_jobs_per_seed: int
    invocations_per_batch_job: int
    seed_job_definition_id: str
    monitor_job_definition_id: str
    batch_job_definition_id: str
    suspended: bool
    tenant_id: str
    create_user_id: str

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> Batch:
        return cls(
            id_=data['id'],
            type_=data['type'],
            total_jobs=data['totalJobs'],
            jobs_created=data['jobsCreated'],
            batch_jobs_per_seed=data['batchJobsPerSeed'],
            invocations_per_batch_job=data['invocationsPerBatchJob'],
            seed_job_definition_id=data['seedJobDefinitionId'],
            monitor_job_definition_id=data['monitorJobDefinitionId'],
            batch_job_definition_id=data['batchJobDefinitionId'],
            suspended=data['suspended'],
            tenant_id=data['tenantId'],
            create_user_id=data['createUserId']
        )


@dataclasses.dataclass
class BatchStats:
    """Data class of batch statistics as returned by the REST api of Camunda."""
    id_: str
    type_: str
    total_jobs: int
    jobs_created: int
    batch_jobs_per_seed: int
    invocations_per_batch_job: int
    seed_job_definition_id: str
    monitor_job_definition_id: str
    batch_job_definition_id: str
    suspended: bool
    tenant_id: str
    create_user_id: str
    remaining_jobs: int
    completed_jobs: int
    failed_jobs: int

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> BatchStats:
        return cls(
            id_=data['id'],
            type_=data['type'],
            total_jobs=data['totalJobs'],
            jobs_created=data['jobsCreated'],
            batch_jobs_per_seed=data['batchJobsPerSeed'],
            invocations_per_batch_job=data['invocationsPerBatchJob'],
            seed_job_definition_id=data['seedJobDefinitionId'],
            monitor_job_definition_id=data['monitorJobDefinitionId'],
            batch_job_definition_id=data['batchJobDefinitionId'],
            suspended=data['suspended'],
            tenant_id=data['tenantId'],
            create_user_id=data['createUserId'],
            remaining_jobs=data['remainingJobs'],
            completed_jobs=data['completedJobs'],
            failed_jobs=data['failedJobs']
        )


class GetList(pycamunda.base.CamundaRequest):

    batch_id = QueryParameter('batchId')
    type_ = QueryParameter('type')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    suspended = QueryParameter('suspended', provide=pycamunda.base.value_is_true)
    sort_by = QueryParameter('sortBy', mapping={'batch_id': 'batchId', 'tenant_id': 'tenantId'})
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
            batch_id: str = None,
            type_: str = None,
            tenant_id_in: typing.Iterable[str] = None,
            without_tenant_id: bool = False,
            suspended: bool = False,
            sort_by: str = None,
            ascending: bool = True,
            first_result: int = None,
            max_results: int = None
    ):
        """Get a list of batches.

        :param url: Camunda Rest engine URL.
        :param batch_id: Filter by id.
        :param type_: Filter by batch type.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Whether to include only batches that belong to no tenant.
        :param suspended: Whether to include only suspended batches.
        :param sort_by: Sort the results by 'batch_id' or 'tenant_id'.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.batch_id = batch_id
        self.type_ = type_
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.suspended = suspended
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results

    def __call__(self, *args, **kwargs) -> typing.Tuple[Batch]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return tuple(Batch.load(batch_json) for batch_json in response.json())


class Count(pycamunda.base.CamundaRequest):

    batch_id = QueryParameter('batchId')
    type_ = QueryParameter('type')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    suspended = QueryParameter('suspended', provide=pycamunda.base.value_is_true)

    def __init__(
            self,
            url: str,
            batch_id: str = None,
            type_: str = None,
            tenant_id_in: typing.Iterable[str] = None,
            without_tenant_id: bool = False,
            suspended: bool = False,
    ):
        """Count batches.

        :param url: Camunda Rest engine URL.
        :param batch_id: Filter by id.
        :param type_: Filter by batch type.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Whether to include only batches that belong to no tenant.
        :param suspended: Whether to include only suspended batches.
        """
        super().__init__(url=url + URL_SUFFIX + '/count')
        self.batch_id = batch_id
        self.type_ = type_
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.suspended = suspended

    def __call__(self, *args, **kwargs) -> int:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return response.json()['count']


class Get(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str = None):
        """Get a batch.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the batch
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> Batch:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return Batch.load(response.json())


class _ActivateSuspend(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    suspended = BodyParameter('suspended')

    def __init__(self, url: str, id_: str, suspended: bool):
        """Activate or Suspend a batch.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the batch.
        :param suspended: Whether to suspend or activate the batch.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/suspended')
        self.id_ = id_
        self.suspended = suspended

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.PUT, *args, **kwargs)


class Activate(_ActivateSuspend):

    def __init__(self, url: str, id_: str):
        """Activate a batch.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the batch.
        """
        super().__init__(url=url, id_=id_, suspended=False)


class Suspend(_ActivateSuspend):

    def __init__(self, url: str, id_: str):
        """Suspend a batch.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the batch.
        """
        super().__init__(url=url, id_=id_, suspended=True)


class Delete(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    cascade = QueryParameter('cascade', provide=pycamunda.base.value_is_true)

    def __init__(self, url: str, id_: str, cascade: bool = False):
        """Delete a batch.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the batch.
        :param cascade: Whether to cascade the deletion to historic batch and historic job logs.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.cascade = cascade

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.DELETE, *args, **kwargs)


class GetStats(pycamunda.base.CamundaRequest):

    batch_id = QueryParameter('batchId')
    type_ = QueryParameter('type')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    suspended = QueryParameter('suspended', provide=pycamunda.base.value_is_true)
    sort_by = QueryParameter('sortBy', mapping={'batch_id': 'batchId', 'tenant_id': 'tenantId'})
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
            batch_id: str = None,
            type_: str = None,
            tenant_id_in: typing.Iterable[str] = None,
            without_tenant_id: bool = False,
            suspended: bool = False,
            sort_by: str = None,
            ascending: bool = True,
            first_result: int = None,
            max_results: int = None
    ):
        """Get batch statistics.

        :param url: Camunda Rest engine URL.
        :param batch_id: Filter by id.
        :param type_: Filter by batch type.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Whether to include only batches that belong to no tenant.
        :param suspended: Whether to include only suspended batches.
        :param sort_by: Sort the results by 'batch_id' or 'tenant_id'.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url=url + URL_SUFFIX + '/statistics')
        self.batch_id = batch_id
        self.type_ = type_
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.suspended = suspended
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results

    def __call__(self, *args, **kwargs) -> typing.Tuple[BatchStats]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return tuple(BatchStats.load(stats_json) for stats_json in response.json())


class CountStats(pycamunda.base.CamundaRequest):

    batch_id = QueryParameter('batchId')
    type_ = QueryParameter('type')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    suspended = QueryParameter('suspended', provide=pycamunda.base.value_is_true)

    def __init__(
            self,
            url: str,
            batch_id: str = None,
            type_: str = None,
            tenant_id_in: typing.Iterable[str] = None,
            without_tenant_id: bool = False,
            suspended: bool = False
    ):
        """Count batch statistics.

        :param url: Camunda Rest engine URL.
        :param batch_id: Filter by id.
        :param type_: Filter by batch type.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Whether to include only batches that belong to no tenant.
        :param suspended: Whether to include only suspended batches.
        """
        super().__init__(url=url + URL_SUFFIX + '/statistics/count')
        self.batch_id = batch_id
        self.type_ = type_
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.suspended = suspended

    def __call__(self, *args, **kwargs) -> typing.Tuple[BatchStats]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return response.json()['count']
