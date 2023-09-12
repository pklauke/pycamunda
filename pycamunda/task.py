# -*- coding: utf-8 -*-

"""This module provides access to the task REST api of Camunda."""

from __future__ import annotations
import datetime as dt
import dataclasses
import enum
import typing

import pycamunda.variable
import pycamunda.base
from pycamunda.request import BodyParameter, PathParameter, QueryParameter

URL_SUFFIX = '/task'


__all__ = [
    'DelegationState', 'Get', 'GetList', 'Claim', 'Unclaim', 'Complete', 'Resolve', 'SetAssignee',
    'Delegate', 'Create', 'Update', 'LocalVariablesGet', 'LocalVariablesGetList',
    'LocalVariablesModify', 'LocalVariablesUpdate', 'LocalVariablesDelete',
    'GetCountByCandidateGroup'
]


@dataclasses.dataclass
class Task:
    """Data class of task as returned by the REST api of Camunda."""
    assignee: str
    case_definition_id: str
    case_execution_id: str
    case_instance_id: str
    delegation_state: str
    description: str
    execution_id: str
    form_key: str
    id_: str
    name: str
    owner: str
    parent_task_id: str
    priority: str
    process_definition_id: str
    process_instance_id: str
    suspended: bool
    task_definition_key: str
    created: str = None
    due: str = None
    follow_up: str = None

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> Task:
        task = cls(
            assignee=data['assignee'],
            case_definition_id=data['caseDefinitionId'],
            case_execution_id=data['caseExecutionId'],
            case_instance_id=data['caseInstanceId'],
            delegation_state=data['delegationState'],
            description=data['description'],
            execution_id=data['executionId'],
            form_key=data['formKey'],
            id_=data['id'],
            name=data['name'],
            owner=data['owner'],
            parent_task_id=data['parentTaskId'],
            priority=data['priority'],
            process_definition_id=data['processDefinitionId'],
            process_instance_id=data['processInstanceId'],
            suspended=data['suspended'],
            task_definition_key=data['taskDefinitionKey'],
        )
        if data['created'] is not None:
            task.created = pycamunda.base.from_isoformat(data['created'])
        if data['due'] is not None:
            task.due = pycamunda.base.from_isoformat(data['due'])
        if data['followUp'] is not None:
            task.follow_up = pycamunda.base.from_isoformat(data['followUp'])

        return task


class DelegationState(enum.Enum):
    pending = 'PENDING'
    resolved = 'RESOLVED'


@dataclasses.dataclass
class IdentityLink:
    """Data class of an identity link related to user tasks as returned by the REST api of
    Camunda.
    """
    user_id: str
    group_id: str
    type_: str

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> IdentityLink:
        return cls(
            user_id=data['userId'],
            group_id=data['groupId'],
            type_=data['type']
        )


@dataclasses.dataclass
class Comment:
    """Data class of a comment that is attached to an user task."""
    id_: str
    user_id: str
    task_id: str
    message: str
    root_process_instance_id: str
    time: dt.datetime = None
    removal_time: dt.datetime = None

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> Comment:
        comment = cls(
            id_=data['id'],
            user_id=data['userId'],
            task_id=data['taskId'],
            message=data['message'],
            root_process_instance_id=data['rootProcessInstanceId']
        )
        if data['time'] is not None:
            comment.time = pycamunda.base.from_isoformat(data['time'])
        if data['removalTime'] is not None:
            comment.removal_time = pycamunda.base.from_isoformat(data['removalTime'])

        return comment


@dataclasses.dataclass
class CountByCandidateGroup:
    """Data class of task count by candidate group."""
    group_name: typing.Optional[str]
    task_count: int

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> CountByCandidateGroup:
        return cls(
            group_name=data['groupName'],
            task_count=int(data['taskCount'])
        )


class Get(pycamunda.base.CamundaRequest):

    id_ = PathParameter("id")

    def __init__(self, url: str, id_: str, timeout: int = 5):
        """Get an user task.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user task.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> Task:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return Task.load(response.json())


class GetList(pycamunda.base.CamundaRequest):

    process_instance_id = QueryParameter('processInstanceId')
    process_instance_id_in = QueryParameter('processInstanceIdIn')
    process_instance_business_key = QueryParameter('processInstanceBusinessKey')
    process_instance_business_key_in = QueryParameter('processInstanceBusinessKeyIn')
    process_instance_business_key_like = QueryParameter('processInstanceBusinessKeyLike')
    process_definition_id = QueryParameter('processDefinitionId')
    process_definition_key = QueryParameter('processDefinitionKey')
    process_definition_key_in = QueryParameter('processDefinitionKeyIn')
    process_definition_name = QueryParameter('processDefinitionName')
    process_definition_name_like = QueryParameter('processDefinitionNameLike')
    execution_id = QueryParameter('executionId')
    case_instance_id = QueryParameter('caseInstanceId')
    case_instance_business_key = QueryParameter('caseInstanceBusinessKey')
    case_instance_business_key_like = QueryParameter('caseInstanceBusinessKeyLike')
    case_definition_id = QueryParameter('caseDefinitionId')
    case_definition_key = QueryParameter('caseDefinitionKey')
    case_instance_name = QueryParameter('caseInstanceName')
    case_instance_name_like = QueryParameter('caseInstanceNameLike')
    case_execution_id = QueryParameter('caseExecutionId')
    activity_instance_id_in = QueryParameter('activityInstanceIdIn')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    assignee = QueryParameter('assignee')
    assignee_like = QueryParameter('assigneeLike')
    assignee_in = QueryParameter('assigneeIn')
    owner = QueryParameter('owner')
    candidate_group = QueryParameter('candidateGroup')
    candidate_user = QueryParameter('candidateUser')
    include_assigned_tasks = QueryParameter('includeAssignedTasks')
    involved_user = QueryParameter('involvedUser')
    assigned = QueryParameter('assigned')
    unassigned = QueryParameter('unassigned')
    task_definition_key = QueryParameter('taskDefinitionKey')
    task_definition_key_in = QueryParameter('taskDefinitionKeyIn')
    task_definition_key_like = QueryParameter('taskDefinitionKeyLike')
    name = QueryParameter('name')
    name_not_equal = QueryParameter('nameNotEqual')
    name_like = QueryParameter('nameLike')
    name_not_like = QueryParameter('nameNotLike')
    description = QueryParameter('description')
    description_like = QueryParameter('descriptionLike')
    priority = QueryParameter('priority')
    max_priority = QueryParameter('maxPriority')
    min_priority = QueryParameter('minPriority')
    due_date = QueryParameter('dueDate')
    due_after = QueryParameter('dueAfter')
    due_before = QueryParameter('dueBefore')
    follow_up_date = QueryParameter('followUpDate')
    follow_up_after = QueryParameter('followUpAfter')
    follow_up_before = QueryParameter('followUpBefore')
    follow_up_before_or_not_existent = QueryParameter('followUpBeforeOrNotExistent')
    created_on = QueryParameter('createdOn')
    created_after = QueryParameter('createdAfter')
    created_before = QueryParameter('createdBefore')
    delegation_state = QueryParameter('delegationState')
    candidate_groups = QueryParameter('candidateGroups')
    with_candidate_groups = QueryParameter(
        'withCandidateGroups', provide=pycamunda.base.value_is_true
    )
    without_candidate_groups = QueryParameter(
        'withoutCandidateGroups', provide=pycamunda.base.value_is_true
    )
    with_candidate_users = QueryParameter(
        'withCandidateUsers', provide=pycamunda.base.value_is_true
    )
    without_candidate_users = QueryParameter(
        'withoutCandidateUsers', provide=pycamunda.base.value_is_true
    )
    active = QueryParameter('active', provide=pycamunda.base.value_is_true)
    suspended = QueryParameter('suspended', provide=pycamunda.base.value_is_true)
    # TODO add variables parameters
    parent_task_id = QueryParameter('parentTaskId')
    sort_by = QueryParameter(
        'sortBy',
        mapping={
            'instance_id': 'instanceId',
            'case_instance_id': 'caseInstanceId',
            'due_date': 'dueDate',
            'execution_id': 'executionId',
            'case_execution_id': 'caseExecutionId',
            'assignee': 'assignee',
            'created': 'created',
            'description': 'description',
            'id': 'id',
            'name': 'name',
            'name_case_insensitive': 'nameCaseInsensitive',
            'priority': 'priority'
        }
    )
    ascending = QueryParameter(
        'sortOrder',
        mapping={True: 'asc', False: 'desc'},
        provide=lambda self, obj, obj_type: vars(obj).get('sort_by', None) is not None
    )
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')
    # TODO add expression parameters, consider explicit addition of each possible expression function

    def __init__(
        self,
        url: str,
        process_instance_id: str = None,
        process_instance_id_in: typing.Iterable[str] = None,
        process_instance_business_key: str = None,
        process_instance_business_key_in: typing.Iterable[str] = None,
        process_instance_business_key_like: str = None,
        process_definition_id: str = None,
        process_definition_key: str = None,
        process_definition_key_in: typing.Iterable[str] = None,
        process_definition_name: str = None,
        process_definition_name_like: str = None,
        execution_id: str = None,
        case_instance_id: str = None,
        case_instance_business_key: str = None,
        case_instance_business_key_like: str = None,
        case_definition_id: str = None,
        case_definition_key: str = None,
        case_instance_name: str = None,
        case_instance_name_like: str = None,
        case_execution_id: str = None,
        activity_instance_id_in: typing.Iterable[str] = None,
        tenant_id_in: typing.Iterable[str] = None,
        without_tenant_id: bool = False,
        assignee: str = None,
        assignee_like: str = None,
        assignee_in: typing.Iterable[str] = None,
        owner: str = None,
        candidate_group: str = None,
        candidate_user: str = None,
        include_assigned_tasks: bool = None,
        involved_user: str = None,
        assigned: bool = None,
        unassigned: bool = None,
        task_definition_key: str = None,
        task_definition_key_in: typing.Iterable[str] = None,
        task_definition_key_like: str = None,
        name: str = None,
        name_not_equal: str = None,
        name_like: str = None,
        name_not_like: str = None,
        description: str = None,
        description_like: str = None,
        priority: int = None,
        max_priority: int = None,
        min_priority: int = None,
        due_date: dt.datetime = None,
        due_after: dt.datetime = None,
        due_before: dt.datetime = None,
        follow_up_date: dt.datetime = None,
        follow_up_after: dt.datetime = None,
        follow_up_before: dt.datetime = None,
        follow_up_before_or_not_existent: dt.datetime = None,
        created_on: dt.datetime = None,
        created_after: dt.datetime = None,
        created_before: dt.datetime = None,
        delegation_state: typing.Union[str, DelegationState] = None,
        candidate_groups: typing.Iterable['str'] = None,
        with_candidate_groups: bool = False,
        without_candidate_groups: bool = False,
        with_candidate_users: bool = False,
        without_candidate_users: bool = False,
        active: bool = False,
        suspended: bool = False,
        parent_task_id: str = None,
        sort_by: str = None,
        ascending: bool = True,
        first_result: int = None,
        max_results: int = None,
        timeout: int = 5
    ):
        """Get a list of user tasks.

        :param url: Camunda Rest engine URL.
        :param process_instance_id: Filter by the process instance id.
        :param process_instance_id_in: Filter whether the process instance id is one of mutliple
                                       ones.
        :param process_instance_business_key: Filter by the business key of the process instance.
        :param process_instance_business_key_in: Filter whether the process instance business key is
                                                 one of multiple ones.
        :param process_instance_business_key_like: Filter by a substring of the process instance
                                                   business key.
        :param process_definition_id: Filter by the process definition id.
        :param process_definition_key: Filter by the process definition key.
        :param process_definition_key_in: Filter whether the the process definition key is one of
                                          multiple ones.
        :param process_definition_name: Filter by the process definition name.
        :param process_definition_name_like: Filter by a substring of the process definition name.
        :param execution_id: Filter by execution id.
        :param case_instance_id: Filter by case instance id.
        :param case_instance_business_key: Filter by case instance business key.
        :param case_instance_business_key_like: Filter by a substring of the case instance business
                                                key.
        :param case_definition_id: Filter by case definition id.
        :param case_definition_key: Filter by case definition key.
        :param case_instance_name: Filter by case instance name.
        :param case_instance_name_like: Filter by a substring of the case instance name.
        :param case_execution_id: Filter by case execution id.
        :param activity_instance_id_in: Filter whether the activity instance id is one of multiple
                                        ones.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Whether to include only tasks that belong to no tenant.
        :param assignee: Filter by assignee.
        :param assignee_like: Filter by a substring of the assignee.
        :param assignee_in: Filter whether the assignee is one of multiple ones.
        :param owner: Filter by owner.
        :param candidate_group: Filter by candidate group.
        :param candidate_user: Filter by candidate user.
        :param include_assigned_tasks: Include only tasks that are assigned to an user.
        :param involved_user: Filter whether a user is involved in the task in some way.
                              (e.g. assigned)
        :param assigned: Filter whether the task is assigned.
        :param unassigned: Filter whether the task is unassigned.
        :param task_definition_key: Filter by task definition key.
        :param task_definition_key_in: Filter whether the task definition key is one of multiple
                                       ones.
        :param task_definition_key_like: Filter by a substring of the task definition key.
        :param name: Filter by name.
        :param name_not_equal: Filter tasks whose names are not equal the provided value.
        :param name_like: Filter by a substring of the name.
        :param name_not_like: Filter tasks whose names do not have the provided value as substring.
        :param description: Filter by description.
        :param description_like: Filter by a substring of the description.
        :param priority: Filter by priority.
        :param max_priority: Filter tasks whose priority is less than or equal the provided value.
        :param min_priority: Filter tasks whose priority is greater than or equal the provided
                             value.
        :param due_date: Filter by due date.
        :param due_after: Include only tasks whose due date expires after the provided date.
        :param due_before: Include only tasks whose due date expires before the provided date.
        :param follow_up_date: Filter by follow up date.
        :param follow_up_after: Include only tasks whose follow up date expires after the provided
                                date.
        :param follow_up_before: Include only tasks whose follow up date expires before the provided
                                 date.
        :param follow_up_before_or_not_existent: Include only tasks whose follow up date expires
                                                 before the provided date or have no follow up date.
        :param created_on: Filter by the creation date.
        :param created_after: Include only tasks whose creation date expires after the provided
                              date.
        :param created_before: Include only tasks whose creation date expires before the provided
                               date.
        :param delegation_state: Filter by delegation state. Valid values are 'PENDING' and
                                 'RESOLVED'.
        :param candidate_groups: Filter whether the candidate group is one of multiple ones.
        :param with_candidate_groups: Filter whether the task has a candidate group.
        :param without_candidate_groups: Filter whether the task has no candidate group.
        :param with_candidate_users: Filter whether the task has candidate users.
        :param without_candidate_users: Filter whether the nas no candidate users.
        :param active: Filter whether the task is active.
        :param suspended: Filter whether the is suspended.
        :param parent_task_id: Filter by parent task id.
        :param sort_by: Sort the results by 'instance_id', 'case_instance_id', 'due_date',
                        'execution_id', 'case_execution_id', 'assignee', 'created', 'description',
                        'id', 'name', 'name_case_insensitive' or 'priority'.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.process_instance_id = process_instance_id
        self.process_instance_id_in = process_instance_id_in
        self.process_instance_business_key = process_instance_business_key
        self.process_instance_business_key_in = process_instance_business_key_in
        self.process_instance_business_key_like = process_instance_business_key_like
        self.process_definition_id = process_definition_id
        self.process_definition_key = process_definition_key
        self.process_definition_key_in = process_definition_key_in
        self.process_definition_name = process_definition_name
        self.process_definition_name_like = process_definition_name_like
        self.execution_id = execution_id
        self.case_instance_id = case_instance_id
        self.case_instance_business_key = case_instance_business_key
        self.case_instance_business_key_like = case_instance_business_key_like
        self.case_definition_id = case_definition_id
        self.case_definition_key = case_definition_key
        self.case_instance_name = case_instance_name
        self.case_instance_name_like = case_instance_name_like
        self.case_execution_id = case_execution_id
        self.activity_instance_id_in = activity_instance_id_in
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.assignee = assignee
        self.assignee_like = assignee_like
        self.assignee_in = assignee_in
        self.owner = owner
        self.candidate_group = candidate_group
        self.candidate_user = candidate_user
        self.include_assigned_tasks = include_assigned_tasks
        self.involved_user = involved_user
        self.assigned = assigned
        self.unassigned = unassigned
        self.task_definition_key = task_definition_key
        self.task_definition_key_in = task_definition_key_in
        self.task_definition_key_like = task_definition_key_like
        self.name = name
        self.name_not_equal = name_not_equal
        self.name_like = name_like
        self.name_not_like = name_not_like
        self.description = description
        self.description_like = description_like
        self.priority = priority
        self.min_priority = min_priority
        self.max_priority = max_priority
        self.due_date = due_date
        self.due_after = due_after
        self.due_before = due_before
        self.follow_up_date = follow_up_date
        self.follow_up_after = follow_up_after
        self.follow_up_before = follow_up_before
        self.follow_up_before_or_not_existent = follow_up_before_or_not_existent
        self.created_on = created_on
        self.created_after = created_after
        self.created_before = created_before
        self.delegation_state = None
        if delegation_state is not None:
            self.delegation_state = DelegationState(delegation_state)
        self.candidate_groups = candidate_groups
        self.with_candidate_groups = with_candidate_groups
        self.without_candidate_groups = without_candidate_groups
        self.with_candidate_users = with_candidate_users
        self.without_candidate_users = without_candidate_users
        self.active = active
        self.suspended = suspended
        self.parent_task_id = parent_task_id
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> typing.Tuple[Task]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return tuple(Task.load(task_json) for task_json in response.json())


class Claim(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    user_id = BodyParameter('userId')

    def __init__(self, url: str, id_: str, user_id: str, timeout: int = 5):
        """Claim a user task for a specific user. Only tasks that are not already claimed by other
        users can be claimed. To change the assignee of a task independently on whether it is
        already claimed by an user, the class 'SetAssignee' can be used.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user task.
        :param user_id: Id of the user to set as assignee for the task.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/claim')
        self.id_ = id_
        self.user_id = user_id
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)


class Unclaim(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str, timeout: int = 5):
        """Unclaim an user task.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user task.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/unclaim')
        self.id_ = id_
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)


class Complete(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    variables = BodyParameter('variables')
    with_variables_in_return = BodyParameter('withVariablesInReturn')

    def __init__(self, url: str, id_: str, with_variables_in_return: bool = False, timeout: int = 5):
        """Complete an user task.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user task.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/complete')
        self.id_ = id_
        self.with_variables_in_return = with_variables_in_return

        self.variables = {}
        self.timeout = timeout

    def add_variable(
        self, name: str, value: typing.Any, type_: str = None, value_info: typing.Any = None
    ) -> None:
        """Add a variable to send to the Camunda process instance.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable.
        :param value_info: Additional information regarding the value type.
        """
        self.variables[name] = {'value': value, 'type': type_, 'valueInfo': value_info}

    def __call__(
        self, *args, **kwargs
    ) -> typing.Optional[typing.Dict[str, pycamunda.variable.Variable]]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)

        if self.with_variables_in_return:
            return {
                name: pycamunda.variable.Variable.load(var_json)
                for name, var_json in response.json().items()
            }


class Resolve(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    variables = BodyParameter('variables')

    def __init__(self, url: str, id_: str, timeout: int = 5):
        """Resolve an user task that was delegated to the current assignee and send it back to the
        original owner. It is necessary that the task was delegated. The assignee of the user task
        will be set back to the owner of the task.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user task.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/resolve')
        self.id_ = id_

        self.variables = {}
        self.timeout = timeout

    def add_variable(
        self, name: str, value: typing.Any, type_: str = None, value_info: typing.Any = None
    ) -> None:
        """Add a variable to send to the Camunda process instance.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable.
        :param value_info: Additional information regarding the value type.
        """
        self.variables[name] = {'value': value, 'type': type_, 'valueInfo': value_info}

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)


class SetAssignee(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    user_id = BodyParameter('userId')

    def __init__(self, url: str, id_: str, user_id: str, timeout: int = 5):
        """Set the assignee for an user task. Overwrites existing assignees.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user task.
        :param user_id: Id of the user to set as assignee for the task.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/assignee')
        self.id_ = id_
        self.user_id = user_id
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)


class Delegate(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    user_id = BodyParameter('userId')

    def __init__(self, url: str, id_: str, user_id: str, timeout: int = 5):
        """Delegate an user task to an user.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user task.
        :param user_id: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/delegate')
        self.id_ = id_
        self.user_id = user_id
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)


class Create(pycamunda.base.CamundaRequest):

    id_ = BodyParameter('id')
    name = BodyParameter('name')
    description = BodyParameter('description')
    assignee = BodyParameter('assignee')
    owner = BodyParameter('owner')
    delegation_state = BodyParameter('delegationState')
    due = BodyParameter('due')
    follow_up = BodyParameter('followUp')
    priority = BodyParameter('priority')
    parent_task_id = BodyParameter('parentTaskId')
    case_instance_id = BodyParameter('caseInstanceId')
    tenant_id = BodyParameter('tenantId')

    def __init__(
        self,
        url: str,
        id_: str,
        name: str = None,
        description: str = None,
        assignee: str = None,
        owner: str = None,
        delegation_state: typing.Union[str, DelegationState] = None,
        due: dt.datetime = None,
        follow_up: dt.datetime = None,
        priority: int = None,
        parent_task_id: str = None,
        case_instance_id: str = None,
        tenant_id: str = None,
        timeout: int = 5
    ):
        """Create an user task.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the task.
        :param name: Name of the task.
        :param description: Description of the task.
        :param assignee: The user the task is assigned to.
        :param owner: The owner of the task.
        :param delegation_state: The delegation state. Valid values are 'RESOLVED' and 'PENDING'.
        :param due: Due date of the task.
        :param follow_up: Follow up date of the task.
        :param priority: Priority of the task.
        :param parent_task_id: Id of the parent task in case this task is a subtask.
        :param case_instance_id: Id of the case instance.
        :param tenant_id: Id of the tenant.
        """
        super().__init__(url=url + URL_SUFFIX + '/create')
        self.id_ = id_
        self.name = name
        self.description = description
        self.assignee = assignee
        self.owner = owner
        self.delegation_state = None
        if delegation_state is not None:
            self.delegation_state = DelegationState(delegation_state)
        self.due = due
        self.follow_up = follow_up
        self.priority = priority
        self.parent_task_id = parent_task_id
        self.case_instance_id = case_instance_id
        self.tenant_id = tenant_id
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)


class Update(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    name = BodyParameter('name')
    description = BodyParameter('description')
    assignee = BodyParameter('assignee')
    owner = BodyParameter('owner')
    delegation_state = BodyParameter('delegationState')
    due = BodyParameter('due')
    follow_up = BodyParameter('followUp')
    priority = BodyParameter('priority')
    parent_task_id = BodyParameter('parentTaskId')
    case_instance_id = BodyParameter('caseInstanceId')
    tenant_id = BodyParameter('tenantId')

    def __init__(
        self,
        url: str,
        id_: str,
        name: str,
        description: str,
        assignee: str,
        owner: str,
        delegation_state: typing.Union[str, DelegationState],
        due: dt.datetime,
        follow_up: dt.datetime,
        priority: int,
        parent_task_id: str,
        case_instance_id: str,
        tenant_id: str,
        timeout: int = 5
    ):
        """Update an user task.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the task.
        :param name: Name of the task.
        :param description: Description of the task.
        :param assignee: The user the task is assigned to.
        :param owner: The owner of the task.
        :param delegation_state: The delegation state. Valid values are 'RESOLVED' and 'PENDING'.
        :param due: Due date of the task.
        :param follow_up: Follow up date of the task.
        :param priority: Priority of the task.
        :param parent_task_id: Id of the parent task in case this task is a subtask.
        :param case_instance_id: Id of the case instance.
        :param tenant_id: Id of the tenant. Cannot be changed. Has to be the same value as the task
                          already has.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_
        self.name = name
        self.description = description
        self.assignee = assignee
        self.owner = owner
        self.delegation_state = None
        if delegation_state is not None:
            self.delegation_state = DelegationState(delegation_state)
        self.due = due
        self.follow_up = follow_up
        self.priority = priority
        self.parent_task_id = parent_task_id
        self.case_instance_id = case_instance_id
        self.tenant_id = tenant_id
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.PUT, *args, **kwargs, timeout=self.timeout)


class IdentityLinksGetList(pycamunda.base.CamundaRequest):

    task_id = PathParameter('id')
    type_ = QueryParameter('type')

    def __init__(self, url: str, task_id: str = None, type_: str = None, timeout: int = 5) -> None:
        """Get the identity links of an user task.

        An identity link is a relationship between an user task and an user or a group. E.g. when
        the user is the assignee / owner or one of the candidate users of the task.

        :param url: Camunda Rest engine URL.
        :param task_id: Id of the task.
        :param type_: Type of the identity link. Can be any custom string. Pre-defined types are
                      'assignee' (user), 'owner' (user) and 'candidate' (user / group).
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/identity-links')
        self.task_id = task_id
        self.type_ = type_
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> typing.Tuple[IdentityLink]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return tuple(IdentityLink.load(link_json) for link_json in response.json())


class IdentityLinksAdd(pycamunda.base.CamundaRequest):

    task_id = PathParameter('id')
    user_id = BodyParameter('userId')
    group_id = BodyParameter('groupId')
    type_ = BodyParameter('type')

    def __init__(
            self, url: str, task_id: str, type_: str, user_id: str = None, group_id: str = None, timeout: int =5
    ):
        """Add an identity link to an user task.

        An identity link is a relationship between an user task and an user or a group. E.g. when
        the user is the assignee / owner or one of the candidate users of the task.

        :param url: Camunda Rest engine URL.
        :param task_id: Id of the task.
        :param user_id: Id of the user. Can not be provided if group_id is provided.
        :param group_id: Id of the groupt. Can not be provided if user_id is provided.
        :param type_: Type of the identity link. Can be any custom string. Pre-defined types are
                      'assignee' (user), 'owner' (user) and 'candidate' (user / group).
        """
        assert (user_id is None) != (group_id is None), (
            'Either \'user_id\' or \'group_id\' has to be provided, not both.'
        )
        super().__init__(url=url + URL_SUFFIX + '/{id}/identity-links')
        self.task_id = task_id
        self.user_id = user_id
        self.group_id = group_id
        self.type_ = type_
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)


class IdentityLinksDelete(pycamunda.base.CamundaRequest):

    task_id = PathParameter('id')
    user_id = BodyParameter('userId')
    group_id = BodyParameter('groupId')
    type_ = BodyParameter('type')

    def __init__(
        self, url: str, task_id: str, type_: str, user_id: str = None, group_id: str = None, timeout: int = 5
    ):
        """Delete an identity link of an user task.

        An identity link is a relationship between an user task and an user or a group. E.g. when
        the user is the assignee / owner or one of the candidate users of the task.

        :param url: Camunda Rest engine URL.
        :param task_id: Id of the task.
        :param user_id: Id of the user. Can not be provided if group_id is provided.
        :param group_id: Id of the groupt. Can not be provided if user_id is provided.
        :param type_: Type of the identity link. Can be any custom string. Pre-defined types are
                      'assignee' (user), 'owner' (user) and 'candidate' (user / group).
        """
        assert (user_id is None) != (group_id is None), (
            'Either \'user_id\' or \'group_id\' has to be provided, not both.'
        )
        super().__init__(url=url + URL_SUFFIX + '/{id}/identity-links/delete')
        self.task_id = task_id
        self.user_id = user_id
        self.group_id = group_id
        self.type_ = type_
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)


class CommentGetList(pycamunda.base.CamundaRequest):

    task_id = PathParameter('id')

    def __init__(self, url: str, task_id: str, timeout: int = 5) -> None:
        """Get the comments for an user task.

        :param url: Camunda Rest engine URL.
        :param task_id: Id of the task.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/comment')
        self.task_id = task_id
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> typing.Tuple[Comment]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return tuple(Comment.load(data=comment_json) for comment_json in response.json())


class CommentGet(pycamunda.base.CamundaRequest):

    task_id = PathParameter('id')
    comment_id = PathParameter('commentId')

    def __init__(self, url: str, task_id: str, comment_id: str, timeout: int = 5) -> None:
        """Get a comment for an user task.

        :param url: Camunda Rest engine URL.
        :param task_id: Id of the task.
        :param comment_id: Id of the comment.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/comment/{commentId}')
        self.task_id = task_id
        self.comment_id = comment_id
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> Comment:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return Comment.load(data=response.json())


class CommentCreate(pycamunda.base.CamundaRequest):

    task_id = PathParameter('id')
    message = BodyParameter('message')

    def __init__(self, url: str, task_id: str, message: str, timeout: int = 5) -> None:
        """Create a comment for an user task.

        :param url: Camunda Rest engine URL.
        :param task_id: Id of the task.
        :param message: Message of the task.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/comment/create')
        self.task_id = task_id
        self.message = message
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> Comment:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)

        return Comment.load(data=response.json())


class LocalVariablesGet(pycamunda.base.CamundaRequest):

    task_id = PathParameter('id')
    var_name = PathParameter('varName')
    deserialize_value = QueryParameter('deserializeValue')

    def __init__(
        self,
        url: str,
        task_id: str,
        var_name: str,
        deserialize_value: bool = False,
        binary: bool = False,
        timeout: int = 5
    ):
        """Get a local variable of an user task.

        Local variables are variables that do only exist in the context of a task.

        :param url: Camunda Rest engine URL.
        :param task_id: Id of the task.
        :param var_name: Name of the variable.
        :param deserialize_value: Whether serializable variable values are deserialized on server
                                  side.
        :param binary: Whether the requested variable is a binary array or file variable.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/localVariables/{varName}')
        self.task_id = task_id
        self.var_name = var_name
        self.deserialize_value = deserialize_value
        self.binary = binary
        self.timeout = timeout

    @property
    def url(self):
        return super().url + ('/data' if self.binary else '')

    def __call__(self, *args, **kwargs) -> pycamunda.variable.Variable:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        if self.binary:
            return response.content
        return pycamunda.variable.Variable.load(data=response.json())


class LocalVariablesGetList(pycamunda.base.CamundaRequest):

    task_id = PathParameter('id')
    deserialize_values = QueryParameter('deserializeValues')

    def __init__(
        self,
        url: str,
        task_id: str,
        deserialize_values: bool = False,
        timeout: int = 5
    ):
        """Get local variables of an user task.

        Local variables are variables that do only exist in the context of a task.

        :param url: Camunda Rest engine URL.
        :param task_id: Id of the task.
        :param deserialize_values: Whether serializable variable values are deserialized on server
                                   side.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/localVariables')
        self.task_id = task_id
        self.deserialize_values = deserialize_values
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> typing.Dict[str, pycamunda.variable.Variable]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return {
            name: pycamunda.variable.Variable.load(data=var_json)
            for name, var_json in response.json().items()
        }


class LocalVariablesModify(pycamunda.base.CamundaRequest):

    task_id = PathParameter('id')
    modifications = BodyParameter('modifications')
    deletions = BodyParameter('deletions')

    def __init__(self, url: str, task_id: str, deletions: typing.Iterable[str] = None, timeout: int = 5):
        """Modify local variables of an user task. This can be either updating or deleting
        variables.

        Local variables are variables that do only exist in the context of a task.

        :param url: Camunda Rest engine URL.
        :param task_id: Id of the task.
        :param deletions: Variables to delete.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/localVariables')
        self.task_id = task_id
        self.deletions = deletions

        self.modifications = {}
        self.timeout = timeout

    def add_variable(
            self, name: str, value: typing.Any, type_: str = None, value_info: typing.Any = None
    ) -> None:
        """Add a variable to modify.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable.
        :param value_info: Additional information regarding the value type.
        """
        self.modifications[name] = {'value': value, 'type': type_, 'valueInfo': value_info}

    def body_parameters(self, apply: typing.Callable = ...) -> typing.Dict[str, typing.Any]:
        params = super().body_parameters(apply=apply)
        deletions = params.get('deletions', [])
        if isinstance(deletions, str):
            params['deletions'] = [deletions]
        else:
            params['deletions'] = list(deletions)
        return params

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)


class LocalVariablesUpdate(pycamunda.base.CamundaRequest):

    task_id = PathParameter('id')
    var_name = PathParameter('varName')
    value = BodyParameter('value')
    type_ = BodyParameter('type')
    value_info = BodyParameter('valueInfo')

    def __init__(
        self,
        url: str,
        task_id: str,
        var_name: str,
        value: typing.Any, type_: str = None,
        value_info: typing.Any = None,
        timeout: int = 5
    ):
        """Update a local variable. May be used with binary and file variables.

        Local variables are variables that do only exist in the context of a task.

        :param url: Camunda Rest engine URL.
        :param task_id: Id of the task.
        :param var_name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable. To send binary variables use the value 'Bytes' and
                      to send the binary value of a file variable use the value 'File' for this
                      parameter.
        :param value_info: Additional information regarding the value type. Ignored if 'type_' is
                           'Bytes' or 'File'.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/localVariables/{varName}')
        self.task_id = task_id
        self.var_name = var_name
        self.value = value
        self.type_ = type_
        self.value_info = value_info
        self.timeout = timeout

    def _is_binary(self):
        return self.type_ in ('File', 'Bytes')

    @property
    def url(self):
        return super().url + ('/data' if self._is_binary() else '')

    def body_parameters(self, apply: typing.Callable = ...):
        if self._is_binary():
            return {'valueType': self.type_}
        return super().body_parameters(apply=apply)

    @property
    def files(self):
        return {'data': self.value}

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        if self._is_binary():
            response = super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs, timeout=self.timeout)
        else:
            response = super().__call__(pycamunda.base.RequestMethod.PUT, *args, **kwargs, timeout=self.timeout)

        if not response:
            pycamunda.base._raise_for_status(response)


class LocalVariablesDelete(pycamunda.base.CamundaRequest):

    task_id = PathParameter('id')
    var_name = PathParameter('varName')

    def __init__(self, url: str, task_id: str, var_name: str, timeout: int = 5):
        """Delete a local variable.

        Local variables are variables that do only exist in the context of a task.

        :param url: Camunda Rest engine URL.
        :param task_id: Id of the task.
        :param var_name: Name of the variable.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/localVariables/{varName}')
        self.task_id = task_id
        self.var_name = var_name
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.DELETE, *args, **kwargs, timeout=self.timeout)


class GetCountByCandidateGroup(pycamunda.base.CamundaRequest):

    def __init__(self, url: str, timeout: int = 5):
        """Get the number of tasks for each candidate group.

        :param url: Camunda Rest engine URL.
        """
        super().__init__(url=url + URL_SUFFIX + '/report/candidate-group-count')
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> typing.Tuple[CountByCandidateGroup]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return tuple(CountByCandidateGroup.load(data=count_json) for count_json in response.json())
