# -*- coding: utf-8 -*-

import datetime as dt

import pytest

import pycamunda.deployment


def test_deployment_load(my_deployment_json):
    deployment = pycamunda.deployment.Deployment.load(my_deployment_json)

    assert deployment.id_ == my_deployment_json['id']
    assert deployment.name == my_deployment_json['name']
    assert deployment.source == my_deployment_json['source']
    assert deployment.tenant_id == my_deployment_json['tenantId']
    assert deployment.deployment_time == dt.datetime(
        year=2000, month=1, day=1, hour=0, minute=0, second=0, tzinfo=dt.timezone.utc
    )


def test_deployment_load_raises_keyerror(my_deployment_json):
    for key in my_deployment_json:
        json_ = dict(my_deployment_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.deployment.Deployment.load(data=json_)
