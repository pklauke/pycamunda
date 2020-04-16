# -*- coding: utf-8 -*-
import pytest

import pycamunda.processdef


def test_activitystats_load(my_activity_stats_json):
    activity_instance = pycamunda.processdef.ActivityStats.load(my_activity_stats_json)

    assert activity_instance.id_ == my_activity_stats_json['id']
    assert activity_instance.instances == my_activity_stats_json['instances']
    assert activity_instance.failed_jobs == my_activity_stats_json['failedJobs']


def test_activitystats_load_raises_keyerror(my_activity_stats_json):
    for key in my_activity_stats_json:
        json = dict(my_activity_stats_json)
        del json[key]
        with pytest.raises(KeyError):
            pycamunda.processdef.ActivityStats.load(data=json)