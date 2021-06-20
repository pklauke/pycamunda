# -*- coding: utf-8 -*-

import pytest

import pycamunda.batch


def test_batchstats_load(my_batchstats_json):
    batch_stats = pycamunda.batch.BatchStats.load(my_batchstats_json)

    assert batch_stats.id_ == my_batchstats_json['id']
    assert batch_stats.type_ == my_batchstats_json['type']
    assert batch_stats.total_jobs == my_batchstats_json['totalJobs']
    assert batch_stats.jobs_created == my_batchstats_json['jobsCreated']
    assert batch_stats.batch_jobs_per_seed == my_batchstats_json['batchJobsPerSeed']
    assert batch_stats.invocations_per_batch_job == my_batchstats_json['invocationsPerBatchJob']
    assert batch_stats.seed_job_definition_id == my_batchstats_json['seedJobDefinitionId']
    assert batch_stats.monitor_job_definition_id == my_batchstats_json['monitorJobDefinitionId']
    assert batch_stats.batch_job_definition_id == my_batchstats_json['batchJobDefinitionId']
    assert batch_stats.suspended == my_batchstats_json['suspended']
    assert batch_stats.tenant_id == my_batchstats_json['tenantId']
    assert batch_stats.create_user_id == my_batchstats_json['createUserId']
    assert batch_stats.remaining_jobs == my_batchstats_json['remainingJobs']
    assert batch_stats.completed_jobs == my_batchstats_json['completedJobs']
    assert batch_stats.failed_jobs == my_batchstats_json['failedJobs']


def test_batchstats_load_raises_keyerror(my_batchstats_json):
    for key in my_batchstats_json:
        json_ = dict(my_batchstats_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.batch.BatchStats.load(json_)
