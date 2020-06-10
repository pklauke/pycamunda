# -*- coding: utf-8 -*-

"""This module provides access to the incident REST api of Camunda."""

from __future__ import annotations
import datetime as dt
import dataclasses
import enum
import typing

import requests

import pycamunda.variable
import pycamunda.base
from pycamunda.request import QueryParameter, PathParameter

URL_SUFFIX = '/incident'


class IncidentType(enum.Enum):
    failed_job = 'failedJob'
    failed_external_task = 'failedExternalTask'


@dataclasses.dataclass
class IncidentTypeCount:
    """Data class of incident type count as returned by the REST api of Camunda."""
    incident_type: IncidentType
    incident_count: int

    @classmethod
    def load(cls, data) -> IncidentTypeCount:
        return cls(
            incident_type=IncidentType(data['incidentType']),
            incident_count=data['incidentCount']
        )


@dataclasses.dataclass
class Incident:
    """Data class of incident as returned by the REST api of Camunda."""
    id_: str
    process_definition_id: str
    process_instance_id: str
    execution_id: str
    incident_type: IncidentType
    activity_id: str
    cause_incident_id: str
    root_cause_incident_id: str
    configuration: str
    tenant_id: str
    incident_message: str
    job_definition_id: str
    incident_timestamp: dt.datetime = None

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> Incident:
        incident = cls(
            id_=data['id'],
            process_definition_id=data['processDefinitionId'],
            process_instance_id=data['processInstanceId'],
            execution_id=data['executionId'],
            incident_type=IncidentType(data['incidentType']),
            activity_id=data['activityId'],
            cause_incident_id=data['causeIncidentId'],
            root_cause_incident_id=data['rootCauseIncidentId'],
            configuration=data['configuration'],
            tenant_id=data['tenantId'],
            incident_message=data['incidentMessage'],
            job_definition_id=data['jobDefinitionId']
        )
        if data['incidentTimestamp'] is not None:
            incident.incident_timestamp = pycamunda.base.from_isoformat(
                data['incidentTimestamp']
            )

        return incident


class Get(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get an incident.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the incident.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> Incident:
        """Send the request."""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return Incident.load(response.json())


class GetList(pycamunda.base.CamundaRequest):

    incident_id = QueryParameter('incidentId')
    incident_type = QueryParameter('incidentType')
    incident_message = QueryParameter('incidentMessage')
    process_definition_id = QueryParameter('processDefinitionId')
    process_definition_key_in = QueryParameter('processDefinitionKeyIn')
    process_instance_id = QueryParameter('processInstanceId')
    execution_id = QueryParameter('executionId')
    activity_id = QueryParameter('activityId')
    cause_incident_id = QueryParameter('causeIncidentId')
    root_cause_incident_id = QueryParameter('rootCauseIncidentId')
    configuration = QueryParameter('configuration')
    tenant_id_in = QueryParameter('tenantIdIn')
    job_definition_id_in = QueryParameter('jobDefinitionIdIn')
    sort_by = QueryParameter(
        'sortBy',
        mapping={
            'incident_id': 'incidentId',
            'incident_message': 'incidentMessage',
            'incident_timestamp': 'incidentTimestamp',
            'incident_type': 'incidentType',
            'execution_id': 'executionId',
            'activity_id': 'activityId',
            'process_instance_id': 'processInstanceId',
            'process_definition_id': 'processDefinitionId',
            'cause_incident_id': 'causeIncidentId',
            'root_cause_incident_id': 'rootCauseIncidentId',
            'configuration': 'configuration',
            'tenant_id': 'tenantId'
        }
    )
    ascending = QueryParameter(
        'sortOrder',
        mapping={True: 'asc', False: 'desc'},
        provide=lambda self, obj, obj_type: vars(obj).get('sort_by', None) is not None
    )

    def __init__(
        self,
        url: str,
        incident_id: str = None,
        incident_type: str = None,
        incident_message: str = None,
        process_definition_id: str = None,
        process_definition_key_in: typing.Iterable[str] = None,
        process_instance_id: str = None,
        execution_id: str = None,
        activity_id: str = None,
        cause_incident_id: str = None,
        root_cause_incident_id: str = None,
        configuration: str = None,
        tenant_id_in: typing.Iterable[str] = None,
        job_definition_id_in: typing.Iterable[str] = None,
        sort_by: str = None,
        ascending: bool = True
    ):
        """Get a list of incidents.

        :param url: Camunda Rest engine URL.
        :param incident_id: Filter by incident id.
        :param incident_type: Filter by incident type. Valid values are 'failedJob' and
                              'failedExternalTask'
        :param incident_message: Filter by incident message.
        :param process_definition_id: Filter by process definition id.
        :param process_definition_key_in: Filter whether the process definition key is one of
                                          multiple ones.
        :param process_instance_id: Filter by process instance id.
        :param execution_id: Filter by execution id.
        :param activity_id: Filter by activity id.
        :param cause_incident_id: Filter by cause incident id.
        :param root_cause_incident_id: Filter by root cause incident id.
        :param configuration: Filter by configuration.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param job_definition_id_in: Filter whether the job definition id is one of multiple ones.
        :param sort_by: Sort the results by 'incident_id', 'incident_message', incident_timestamp',
                        'incident_type', 'execution_id', 'activity_id', 'process_instance_id',
                        'process_definition_id', 'cause_incident_id', 'root_cause_incident_id',
                        'configuration' or 'tenant_id'.
        :param ascending: Sort order.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.incident_id = incident_id
        self.incident_type = incident_type
        self.incident_message = incident_message
        self.process_definition_id = process_definition_id
        self.process_definition_key_in = process_definition_key_in
        self.process_instance_id = process_instance_id
        self.execution_id = execution_id
        self.activity_id = activity_id
        self.cause_incident_id = cause_incident_id
        self.root_cause_incident_id = root_cause_incident_id
        self.configuration = configuration
        self.tenant_id_in = tenant_id_in
        self.job_definition_id_in = job_definition_id_in
        self.sort_by = sort_by
        self.ascending = ascending

    def __call__(self, *args, **kwargs) -> typing.Tuple[Incident]:
        """Send the request."""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return tuple(Incident.load(incident_json) for incident_json in response.json())


class Resolve(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Resolve an incident.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the incident.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        try:
            response = requests.delete(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)
