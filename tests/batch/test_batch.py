# -*- coding: utf-8 -*-

import pytest

import pycamunda.batch


def test_batch_load(my_batch_json):
    batch = pycamunda.batch.Batch.load(my_batch_json)

    assert batch.id_ == my_batch_json['id']
    assert batch.type_ == my_batch_json['type']
    assert batch.total_jobs == my_batch_json['totalJobs']
    assert batch.jobs_created == my_batch_json['jobsCreated']
    assert batch.batch_jobs_per_seed == my_batch_json['batchJobsPerSeed']
    assert batch.invocations_per_batch_job == my_batch_json['invocationsPerBatchJob']
    assert batch.seed_job_definition_id == my_batch_json['seedJobDefinitionId']
    assert batch.monitor_job_definition_id == my_batch_json['monitorJobDefinitionId']
    assert batch.batch_job_definition_id == my_batch_json['batchJobDefinitionId']
    assert batch.suspended == my_batch_json['suspended']
    assert batch.tenant_id == my_batch_json['tenantId']
    assert batch.create_user_id == my_batch_json['createUserId']


def test_batch_load_raises_keyerror(my_batch_json):
    for key in my_batch_json:
        json_ = dict(my_batch_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.batch.Batch.load(json_)
