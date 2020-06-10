# -*- coding: utf-8 -*-

"""This module provides access to the batch REST api of Camunda"""

from __future__ import annotations
import dataclasses
import typing


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
