# -*- coding: utf-8 -*-

import datetime as dt

import pycamunda.filter
import pycamunda.task


def test_criteria_params_process_instance_criteria():
    criteria = pycamunda.filter._Criteria(url='')
    criteria.add_process_instance_criteria(
        id_='anId', business_key='aKey', business_key_like='aKe'
    )

    assert criteria.process_instance_id == 'anId'
    assert criteria.process_instance_business_key == 'aKey'
    assert criteria.process_instance_business_key_like == 'aKe'


def test_criteria_params_process_definition_criteria():
    criteria = pycamunda.filter._Criteria(url='')
    criteria.add_process_definition_criteria(
        id_='anId', key='aKey', key_in=[], name='aName', name_like='aNam'
    )

    assert criteria.process_definition_id == 'anId'
    assert criteria.process_definition_key == 'aKey'
    assert criteria.process_definition_key_in == []
    assert criteria.process_definition_name == 'aName'
    assert criteria.process_definition_name_like == 'aNam'


def test_criteria_params_case_instance_criteria():
    criteria = pycamunda.filter._Criteria(url='')
    criteria.add_case_instance_criteria(
        id_='anId', business_key='aKey', business_key_like='aKe'
    )

    assert criteria.case_instance_id == 'anId'
    assert criteria.case_instance_business_key == 'aKey'
    assert criteria.case_instance_business_key_like == 'aKe'


def test_criteria_params_case_definition_criteria():
    criteria = pycamunda.filter._Criteria(url='')
    criteria.add_case_definition_criteria(
        id_='anId', key='aKey', name='aName', name_like='aNam'
    )

    assert criteria.case_definition_id == 'anId'
    assert criteria.case_definition_key == 'aKey'
    assert criteria.case_definition_name == 'aName'
    assert criteria.case_definition_name_like == 'aNam'


def test_criteria_params_other_criteria():
    criteria = pycamunda.filter._Criteria(url='')
    criteria.add_other_criteria(
        active=True, activity_instance_id_in=[], execution_id='anExecutionId'
    )

    assert criteria.active is True
    assert criteria.activity_instance_id_in == []
    assert criteria.execution_id == 'anExecutionId'


def test_criteria_params_user_criteria():
    criteria = pycamunda.filter._Criteria(url='')
    criteria.add_user_criteria(
        assignee='anAssignee',
        assignee_in=[],
        assignee_like='anAssigne',
        task_owner='anOwner',
        candidate_user='anUser',
        involved_user='anotherUser',
        unassigned=True,
        delegation_state='PENDING'
    )

    assert criteria.assignee == 'anAssignee'
    assert criteria.assignee_in == []
    assert criteria.assignee_like == 'anAssigne'
    assert criteria.task_owner == 'anOwner'
    assert criteria.candidate_user == 'anUser'
    assert criteria.involved_user == 'anotherUser'
    assert criteria.unassigned is True
    assert criteria.delegation_state == pycamunda.task.DelegationState.pending


def test_criteria_params_task_criteria():
    criteria = pycamunda.filter._Criteria(url='')
    criteria.add_task_criteria(
        definition_key='aKey',
        definition_key_in=[],
        definition_key_like='aKe',
        task_name='aName',
        task_name_like='aNam',
        description='aDescription',
        description_like='aDescriptio',
        priority=10,
        max_priority=50,
        min_priority=5,
        tenant_id_in=[],
        without_tenant_id=True
    )

    assert criteria.task_definition_key == 'aKey'
    assert criteria.task_definition_key_in == []
    assert criteria.task_definition_key_like == 'aKe'
    assert criteria.task_name == 'aName'
    assert criteria.task_name_like == 'aNam'
    assert criteria.description == 'aDescription'
    assert criteria.description_like == 'aDescriptio'
    assert criteria.priority == 10
    assert criteria.max_priority == 50
    assert criteria.min_priority == 5
    assert criteria.tenant_id_in == []
    assert criteria.without_tenant_id is True


def test_criteria_params_datetime_criteria():
    criteria = pycamunda.filter._Criteria(url='')
    criteria.add_datetime_criteria(
        created_before=dt.datetime(year=2020, month=1, day=1),
        created_after=dt.datetime(year=2020, month=1, day=1),
        due_before=dt.datetime(year=2020, month=1, day=1),
        due_after=dt.datetime(year=2020, month=1, day=1),
        follow_up_after=dt.datetime(year=2020, month=1, day=1),
        follow_up_before=dt.datetime(year=2020, month=1, day=1),
        follow_up_before_or_not_existent=dt.datetime(year=2020, month=1, day=1)
    )

    assert criteria.created_before == dt.datetime(year=2020, month=1, day=1)
    assert criteria.created_after == dt.datetime(year=2020, month=1, day=1)
    assert criteria.due_before == dt.datetime(year=2020, month=1, day=1)
    assert criteria.due_after == dt.datetime(year=2020, month=1, day=1)
    assert criteria.follow_up_before == dt.datetime(year=2020, month=1, day=1)
    assert criteria.follow_up_after == dt.datetime(year=2020, month=1, day=1)
    assert criteria.follow_up_before_or_not_existent == dt.datetime(year=2020, month=1, day=1)
