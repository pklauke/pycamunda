# -*- coding: utf-8 -*-

import pytest

import pycamunda.processdef


def test_processinstancestats_load(my_process_instance_stats_json):
    instance_stats = pycamunda.processdef.ProcessInstanceStats.load(my_process_instance_stats_json)

    assert instance_stats.id_ == my_process_instance_stats_json['id']
    assert instance_stats.instances == my_process_instance_stats_json['instances']
    assert instance_stats.failed_jobs == my_process_instance_stats_json['failedJobs']
    assert instance_stats.definition == pycamunda.processdef.ProcessDefinition.load(
        my_process_instance_stats_json['definition']
    )
    assert instance_stats.incidents == my_process_instance_stats_json['incidents']


def test_processinstancestats_load_raises_keyerror(my_process_instance_stats_json):
    for key in my_process_instance_stats_json:
        json = dict(my_process_instance_stats_json)
        del json[key]
        with pytest.raises(KeyError):
            pycamunda.processdef.ProcessInstanceStats.load(data=json)
