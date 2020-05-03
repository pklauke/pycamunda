# -*- coding: utf-8 -*-

import pytest

import pycamunda.processdef


def test_processdefinition_load(my_process_definition_json):
    process_instance = pycamunda.processdef.ProcessDefinition.load(my_process_definition_json)

    assert process_instance.id_ == my_process_definition_json['id']
    assert process_instance.key == my_process_definition_json['key']
    assert process_instance.category == my_process_definition_json['category']
    assert process_instance.description == my_process_definition_json['description']
    assert process_instance.name == my_process_definition_json['name']
    assert process_instance.version == my_process_definition_json['version']
    assert process_instance.resource == my_process_definition_json['resource']
    assert process_instance.deployment_id == my_process_definition_json['deploymentId']
    assert process_instance.diagram == my_process_definition_json['diagram']
    assert process_instance.suspended == my_process_definition_json['suspended']
    assert process_instance.tenant_id == my_process_definition_json['tenantId']
    assert process_instance.version_tag == my_process_definition_json['versionTag']
    assert process_instance.history_time_to_live == my_process_definition_json['historyTimeToLive']
    assert process_instance.startable_in_tasklist == my_process_definition_json[
        'startableInTasklist']


def test_processdefinition_load_raises_keyerror(my_process_definition_json):
    for key in my_process_definition_json:
        json_ = dict(my_process_definition_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.processdef.ProcessDefinition.load(data=json_)
