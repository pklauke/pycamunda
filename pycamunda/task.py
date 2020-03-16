# -*- coding: utf-8 -*-

"""This module provides access to the task REST api of Camunda."""

import dataclasses


@dataclasses.dataclass
class Task:
    assignee: str
    case_definition_id: str
    case_execution_id: str
    case_instance_id: str
    created: str
    delegation_state: str
    description: str
    due: str
    execution_id: str
    follow_up: str
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

    @classmethod
    def load(cls, data):
        return cls(
            assignee=data['assignee'],
            case_definition_id=data['caseDefinitionId'],
            case_execution_id=data['caseExecutionId'],
            case_instance_id=data['caseInstanceId'],
            created=data['created'],
            delegation_state=data['delegationState'],
            description=data['description'],
            due=data['due'],
            execution_id=data['executionId'],
            follow_up=data['followUp'],
            form_key=data['formKey'],
            id_=data['id'],
            name=data['name'],
            owner=data['owner'],
            parent_task_id=data['parentTaskId'],
            priority=data['priority'],
            process_definition_id=data['processDefinitionId'],
            process_instance_id=data['processInstanceId'],
            suspended=data['suspended'],
            task_definition_key=data['taskDefinitionKey']
        )
