# -*- coding: utf-8 -*-

import datetime as dt

import pytest


SOME_DAY = dt.datetime(
    year=2000, month=1, day=1, hour=1, minute=1, second=1, tzinfo=dt.timezone.utc
)


@pytest.fixture
def my_task_json():
    return {
        'assignee': 'anAssignee',
        'caseDefinitionId': 'aCaseDefinitionId',
        'caseExecutionId': 'aCaseExecutionId',
        'caseInstanceId': 'anInstanceId',
        'delegationState': 'PENDING',
        'description': 'aDescription',
        'executionId': 'anExecutionId',
        'formKey': 'aFormKey',
        'id': 'anId',
        'name': 'aName',
        'owner': 'anOwner',
        'parentTaskId': 'aTaskId',
        'priority': 10,
        'processDefinitionId': 'aDefinitionid',
        'processInstanceId': 'aProcessInstanceId',
        'suspended': True,
        'taskDefinitionKey': 'aDefinitionKey',
        'created': '2000-01-01T01:01:01.000+0000',
        'due': '2000-01-01T01:01:01.000+0000',
        'followUp': '2000-01-01T01:01:01.000+0000'
    }


@pytest.fixture
def my_comment_json():
    return {
        'id': 'anId',
        'userId': 'anUserId',
        'taskId': 'aTaskId',
        'time': '2000-01-01T01:01:01.000+0000',
        'message': 'aMessage',
        'removalTime': '2000-01-01T01:01:01.000+0000',
        'rootProcessInstanceId': 'anInstanceId'
    }


@pytest.fixture
def getlist_input():
    return {
        'process_instance_id': 'anInstanceId',
        'process_instance_id_in': [],
        'process_instance_business_key': 'aBusinessKey',
        'process_instance_business_key_in': [],
        'process_instance_business_key_like': 'aBusinessKe',
        'process_definition_id': 'aDefinitionId',
        'process_definition_key': 'aDefinitionKey',
        'process_definition_key_in': [],
        'process_definition_name': 'aDefinitionName',
        'process_definition_name_like': 'aDefinitionNam',
        'execution_id': 'anExecutionId',
        'case_instance_id': 'anInstanceId',
        'case_instance_business_key': 'aCaseInstanceBusinessKey',
        'case_instance_business_key_like': 'aCaseInstanceBusinessKey',
        'case_definition_id': 'aCaseDefinitionId',
        'case_definition_key': 'aCaseDefinitionKey',
        'case_instance_name': 'aCaseInstanceName',
        'case_instance_name_like': 'aCaseInstanceNam',
        'case_execution_id': 'aCaseExecutionId',
        'activity_instance_id_in': [],
        'tenant_id_in': [],
        'without_tenant_id': True,
        'assignee': 'anAssignee',
        'assignee_like': 'anAssigne',
        'assignee_in': [],
        'owner': 'anOwner',
        'candidate_group': 'aCandidateGroup',
        'candidate_user': 'aCandidateUser',
        'include_assigned_tasks': True,
        'involved_user': 'anInvolvedUser',
        'assigned': True,
        'unassigned': False,
        'task_definition_key': 'aTaskDefinitionKey',
        'task_definition_key_in': [],
        'task_definition_key_like': 'ATaskDefinitionKe',
        'name': 'aName',
        'name_not_equal': 'anotherName',
        'name_like': 'aNam',
        'name_not_like': 'anotherNam',
        'description': 'aDescription',
        'description_like': 'aDescriptio',
        'priority': 50,
        'max_priority': 100,
        'min_priority': 10,
        'due_date': SOME_DAY,
        'due_after': SOME_DAY,
        'due_before': SOME_DAY,
        'follow_up_date': SOME_DAY,
        'follow_up_after': SOME_DAY,
        'follow_up_before': SOME_DAY,
        'follow_up_before_or_not_existent': SOME_DAY,
        'created_on': SOME_DAY,
        'created_after': SOME_DAY,
        'created_before': SOME_DAY,
        'delegation_state': 'PENDING',
        'candidate_groups': [],
        'with_candidate_groups': True,
        'without_candidate_groups': True,
        'with_candidate_users': True,
        'without_candidate_users': True,
        'active': True,
        'suspended': True,
        'parent_task_id': 'aParentTaskId',
        'sort_by': 'instance_id',
        'ascending': False,
        'first_result': 1,
        'max_results': 10
    }


@pytest.fixture
def getlist_output():
    return {
        'processInstanceId': 'anInstanceId',
        'processInstanceIdIn': [],
        'processInstanceBusinessKey': 'aBusinessKey',
        'processInstanceBusinessKeyIn': [],
        'processInstanceBusinessKeyLike': 'aBusinessKe',
        'processDefinitionId': 'aDefinitionId',
        'processDefinitionKey': 'aDefinitionKey',
        'processDefinitionKeyIn': [],
        'processDefinitionName': 'aDefinitionName',
        'processDefinitionNameLike': 'aDefinitionNam',
        'executionId': 'anExecutionId',
        'caseInstanceId': 'anInstanceId',
        'caseInstanceBusinessKey': 'aCaseInstanceBusinessKey',
        'caseInstanceBusinessKeyLike': 'aCaseInstanceBusinessKey',
        'caseDefinitionId': 'aCaseDefinitionId',
        'caseDefinitionKey': 'aCaseDefinitionKey',
        'caseInstanceName': 'aCaseInstanceName',
        'caseInstanceNameLike': 'aCaseInstanceNam',
        'caseExecutionId': 'aCaseExecutionId',
        'activityInstanceIdIn': [],
        'tenantIdIn': [],
        'withoutTenantId': 'true',
        'assignee': 'anAssignee',
        'assigneeLike': 'anAssigne',
        'assigneeIn': [],
        'owner': 'anOwner',
        'candidateGroup': 'aCandidateGroup',
        'candidateUser': 'aCandidateUser',
        'includeAssignedTasks': 'true',
        'involvedUser': 'anInvolvedUser',
        'assigned': 'true',
        'unassigned': 'false',
        'taskDefinitionKey': 'aTaskDefinitionKey',
        'taskDefinitionKeyIn': [],
        'taskDefinitionKeyLike': 'ATaskDefinitionKe',
        'name': 'aName',
        'nameNotEqual': 'anotherName',
        'nameLike': 'aNam',
        'nameNotLike': 'anotherNam',
        'description': 'aDescription',
        'descriptionLike': 'aDescriptio',
        'priority': 50,
        'maxPriority': 100,
        'minPriority': 10,
        'dueDate': '2000-01-01T01:01:01.000+0000',
        'dueAfter': '2000-01-01T01:01:01.000+0000',
        'dueBefore': '2000-01-01T01:01:01.000+0000',
        'followUpDate': '2000-01-01T01:01:01.000+0000',
        'followUpAfter': '2000-01-01T01:01:01.000+0000',
        'followUpBefore': '2000-01-01T01:01:01.000+0000',
        'followUpBeforeOrNotExistent': '2000-01-01T01:01:01.000+0000',
        'createdOn': '2000-01-01T01:01:01.000+0000',
        'createdAfter': '2000-01-01T01:01:01.000+0000',
        'createdBefore': '2000-01-01T01:01:01.000+0000',
        'delegationState': 'PENDING',
        'candidateGroups': [],
        'withCandidateGroups': 'true',
        'withoutCandidateGroups': 'true',
        'withCandidateUsers': 'true',
        'withoutCandidateUsers': 'true',
        'active': 'true',
        'suspended': 'true',
        'parentTaskId': 'aParentTaskId',
        'sortBy': 'instanceId',
        'sortOrder': 'desc',
        'firstResult': 1,
        'maxResults': 10
    }


@pytest.fixture
def task_input():
    return {
        'name': 'aName',
        'description': 'aDescription',
        'assignee': 'anAssignee',
        'owner': 'anOwner',
        'delegation_state': 'PENDING',
        'due': SOME_DAY,
        'follow_up': SOME_DAY,
        'priority': 10,
        'parent_task_id': 'aTaskId',
        'case_instance_id': 'anInstanceId',
        'tenant_id': 'aTenantId'
    }


@pytest.fixture
def task_output():
    return {
        'name': 'aName',
        'description': 'aDescription',
        'assignee': 'anAssignee',
        'owner': 'anOwner',
        'delegationState': 'PENDING',
        'due': '2000-01-01T01:01:01.000+0000',
        'followUp': '2000-01-01T01:01:01.000+0000',
        'priority': 10,
        'parentTaskId': 'aTaskId',
        'caseInstanceId': 'anInstanceId',
        'tenantId': 'aTenantId'
    }


@pytest.fixture
def my_identitylink_json():
    return {
        'userId': 'anUserId',
        'groupId': 'aGroupId',
        'type': 'assignee'
    }


@pytest.fixture
def my_countbycandidategroup_json():
    return {
        'groupName': 'myGroup',
        'taskCount': 1
    }
