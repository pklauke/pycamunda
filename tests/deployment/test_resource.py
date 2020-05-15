# -*- coding: utf-8 -*-

import pytest

import pycamunda.deployment


def test_resource_load():
    resource = pycamunda.deployment.Resource.load(
        {'id': 'anId', 'name': 'aName', 'deploymentId': 'aDeploymentId'}
    )

    assert resource.id_ == 'anId'
    assert resource.name == 'aName'
    assert resource.deployment_id == 'aDeploymentId'


def test_resource_load_raises_keyerror():
    resource_json = {'id': 'anId', 'name': 'aName', 'deploymendId': 'aDeploymentId'}
    for key in resource_json:
        json_ = dict(resource_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.deployment.Resource.load(data=json_)
