# -*- coding: utf-8 -*-

"""This module provides activity instance data classes as returned by the REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing

import pycamunda.incident


@dataclasses.dataclass
class TransitionInstance:
    """Data class of transition instance as returned by the REST api of Camunda."""
    id_: str
    activity_id: str
    activity_name: str
    activity_type: str
    process_instance_id: str
    process_definition_id: str
    execution_ids: typing.Tuple[str]
    incident_ids: typing.Tuple[str]
    incidents: typing.Tuple[pycamunda.incident.IncidentTypeCount]

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> TransitionInstance:
        return cls(
            id_=data['id'],
            activity_id=data['activityId'],
            activity_name=data['activityName'],
            activity_type=data['activityType'],
            process_instance_id=data['processInstanceId'],
            process_definition_id=data['processDefinitionId'],
            execution_ids=tuple(data['executionId']),
            incident_ids=tuple(data['incidentIds']),
            incidents=tuple(
                pycamunda.incident.IncidentTypeCount.load(incident_json)
                for incident_json in data['incidents'])
        )


@dataclasses.dataclass
class ActivityInstance:
    """Data class of activity instance as returned by the REST api of Camunda."""
    id_: str
    parent_activity_instance_id: str
    activity_id: str
    activity_name: str
    activity_type: str
    process_instance_id: str
    process_definition_id: str
    child_activity_instances: typing.Tuple[ActivityInstance]
    child_transition_instances: typing.Tuple[TransitionInstance]
    execution_ids: typing.Tuple[str]
    name: str
    incident_ids: typing.Tuple[str] = None
    incidents: typing.Tuple[pycamunda.incident.IncidentTypeCount] = None

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> ActivityInstance:
        activity_instance = cls(
            id_=data['id'],
            parent_activity_instance_id=data['parentActivityInstanceId'],
            activity_id=data['activityId'],
            activity_name=data['activityName'],
            activity_type=data['activityType'],
            process_instance_id=data['processInstanceId'],
            process_definition_id=data['processDefinitionId'],
            child_activity_instances=tuple(
                cls.load(activity_json) for activity_json in data['childActivityInstances']
            ),
            child_transition_instances=tuple(
                TransitionInstance.load(transition_json)
                for transition_json in data['childTransitionInstances']
            ),
            execution_ids=tuple(data['executionIds']),
            name=data['name']
        )
        try:
            activity_instance.incident_ids = tuple(data['incidentIds'])
        except KeyError:
            pass
        try:
            activity_instance.incidents = tuple(
                pycamunda.incident.IncidentTypeCount.load(incident_json)
                for incident_json in data['incidents']
            )
        except KeyError:
            pass

        return activity_instance
