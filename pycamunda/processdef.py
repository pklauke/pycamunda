# -*- coding: utf-8 -*-

"""This module provides access to the process definition REST api of Camunda."""

from __future__ import annotations
import datetime as dt
import typing
import dataclasses

import requests

import pycamunda.variable
import pycamunda.processinst
import pycamunda.batch
import pycamunda.incident
import pycamunda.instruction
import pycamunda.base
from pycamunda.request import QueryParameter, PathParameter, BodyParameter, BodyParameterContainer

URL_SUFFIX = '/process-definition'


@dataclasses.dataclass
class ProcessDefinition:
    """Data class of process definition as returned by the REST api of Camunda."""
    id_: str
    key: str
    category: str
    description: str
    name: str
    version: int
    resource: str
    deployment_id: str
    diagram: str
    suspended: bool
    tenant_id: str
    version_tag: str
    history_time_to_live: int
    startable_in_tasklist: bool

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> ProcessDefinition:
        return cls(
            id_=data['id'],
            key=data['key'],
            category=data['category'],
            description=data['description'],
            name=data['name'],
            version=data['version'],
            resource=data['resource'],
            deployment_id=data['deploymentId'],
            diagram=data['diagram'],
            suspended=data['suspended'],
            tenant_id=data['tenantId'],
            version_tag=data['versionTag'],
            history_time_to_live=data['historyTimeToLive'],
            startable_in_tasklist=data['startableInTasklist']
        )


@dataclasses.dataclass
class ActivityStats:
    """Data class of activity statistics as returned by the REST api of Camunda."""
    id_: str
    instances: int
    failed_jobs: int
    incidents: typing.Iterable[pycamunda.incident.IncidentTypeCount]

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> ActivityStats:
        return cls(
            id_=data['id'],
            instances=data['instances'],
            failed_jobs=data['failedJobs'],
            incidents=tuple(
                pycamunda.incident.IncidentTypeCount.load(incident_data)
                for incident_data in data['incidents']
            )
        )


@dataclasses.dataclass
class ProcessInstanceStats:
    """Data class of process instance statistics as returned by the REST api of Camunda."""
    id_: str
    instances: int
    failed_jobs: int
    definition: ProcessDefinition
    incidents: typing.Iterable[pycamunda.incident.IncidentTypeCount]

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> ProcessInstanceStats:
        return cls(
            id_=data['id'],
            instances=data['instances'],
            failed_jobs=data['failedJobs'],
            definition=ProcessDefinition.load(data['definition']),
            incidents=tuple(
                pycamunda.incident.IncidentTypeCount.load(incident_data)
                for incident_data in data['incidents']
            )
        )


class GetActivityInstanceStats(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')

    failed_jobs = QueryParameter('failedJobs')
    incidents = QueryParameter('incidents', provide=pycamunda.base.value_is_true)
    incidents_for_type = QueryParameter('incidentsForType')

    def __init__(
        self,
        url: str,
        id_: str = None,
        key: str = None,
        tenant_id: str = None,
        failed_jobs: bool = None,
        incidents: bool = False,
        incidents_for_type: typing.Union[str, pycamunda.incident.IncidentType] = None
    ):
        """Get runtime statistics for a process definition. Does not include historic data.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process definition.
        :param key: Key of the process definition.
        :param tenant_id: Id of the tenant the process definition belongs to.
        :param failed_jobs: Whether the number of failed jobs should be included.
        :param incidents: Whether to include the number of incidents.
        :param incidents_for_type: Include only incidents of a specific type.
        """
        if incidents and incidents_for_type is not None:
            raise pycamunda.PyCamundaException(
                'Either \'incidents\' or \'incidents_for_type\' can be provided, not both.'
            )
        super().__init__(url=url + URL_SUFFIX + '/{path}/statistics')
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id
        self.failed_jobs = failed_jobs
        self.incidents = incidents
        self.incident_type = None
        if incidents_for_type is not None:
            self.incidents_for_type = pycamunda.incident.IncidentType(incidents_for_type)

    @property
    def url(self):
        if self.id_ is not None:
            return self._url.format(path=self.id_)
        if self.tenant_id is not None:
            return self._url.format(path=f'key/{self.key}/tenant-id/{self.tenant_id}')
        return self._url.format(path=f'key/{self.key}')

    def __call__(self, *args, **kwargs) -> typing.Tuple[ActivityStats]:
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return tuple(ActivityStats.load(activity_json) for activity_json in response.json())


class GetProcessDiagram(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')

    def __init__(self, url: str, id_: str = None, key: str = None, tenant_id: str = None):
        """Get the diagram of a process definition.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process definition.
        :param key: Key of the process definition.
        """
        super().__init__(url=url + URL_SUFFIX + '/{path}/diagram')
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id

    @property
    def url(self):
        if self.id_ is not None:
            return self._url.format(path=self.id_)
        if self.tenant_id is not None:
            return self._url.format(path=f'key/{self.key}/tenant-id/{self.tenant_id}')
        return self._url.format(path=f'key/{self.key}')

    def __call__(self, *args, **kwargs):
        """Send the request."""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return response.content


class Count(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('processDefinitionId')
    id_in = QueryParameter('processDefinitionIdIn')
    name = QueryParameter('name')
    name_like = QueryParameter('nameLike')
    deployment_id = QueryParameter('deploymentId')
    key = QueryParameter('key')
    key_in = QueryParameter('keysIn')
    key_like = QueryParameter('keyLike')
    category = QueryParameter('category')
    category_like = QueryParameter('categoryLike')
    version = QueryParameter('version')
    latest_version = QueryParameter('latestVersion', provide=pycamunda.base.value_is_true)
    resource_name = QueryParameter('resourceName')
    resource_name_like = QueryParameter('resourceNameLike')
    startable_by = QueryParameter('startableBy')
    active = QueryParameter('active', provide=pycamunda.base.value_is_true)
    suspended = QueryParameter('suspended', provide=pycamunda.base.value_is_true)
    incident_id = QueryParameter('incidentId')
    incident_type = QueryParameter('incidentType')
    incident_message = QueryParameter('incidentMessage')
    incident_message_like = QueryParameter('incidentMessageLike')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    include_without_tenant_id = QueryParameter(
        'includeProcessDefinitionsWithoutTenantId',
        provide=pycamunda.base.value_is_true
    )
    version_tag = QueryParameter('versionTag')
    version_tag_like = QueryParameter('versionTagLike')
    without_version_tag = QueryParameter('withoutVersionTag')
    startable_in_tasklist = QueryParameter('startableInTasklist')
    not_startable_in_tasklist = QueryParameter('notStartableInTasklist')
    startable_permission_check = QueryParameter(
        'startablePermissionCheck',
        mapping={True: 'true', False: 'false'}
    )

    def __init__(
        self,
        url: str,
        id_: str = None,
        id_in: typing.Iterable[str] = None,
        name: str = None,
        name_like: str = None,
        deployment_id: str = None,
        key: str = None,
        key_in: typing.Iterable[str] = None,
        key_like: str = None,
        category: str = None,
        category_like: str = None,
        version: int = None,
        latest_version: bool = False,
        resource_name: str = None,
        resource_name_like: str = None,
        startable_by: str = None,
        active: bool = False,
        suspended: bool = False,
        incident_id: str = None,
        incident_type: typing.Union[str, pycamunda.incident.IncidentType] = None,
        incident_message: str = None,
        incident_message_like: str = None,
        tenant_id_in: typing.Iterable[str] = None,
        without_tenant_id: bool = False,
        include_without_tenant_id: bool = False,
        version_tag: str = None,
        version_tag_like: str = None,
        without_version_tag: bool = None,
        startable_in_tasklist: bool = None,
        startable_permission_check: bool = None,
        not_startable_in_tasklist: bool = None,
    ):
        """Count process definitions.

        :param url: Camunda Rest engine URL.
        :param id_: Filter by id.
        :param id_in: Filter whether the id is one of multiple ones.
        :param name: Filter by name.
        :param name_like: Filter by a substring of the name.
        :param deployment_id: Filter by deployment id.
        :param key: Key of the process definition.
        :param key_in: Filter whether the key is one of multiple ones.
        :param key_like: Filter by a substring of the key.
        :param category: Filter by category.
        :param category_like: Filter by a substring of the category.
        :param version: Filter by version.
        :param latest_version: Whether to include only the latest versions.
        :param resource_name: Filter by resource name.
        :param resource_name_like: Filter by a substring of the resource name.
        :param startable_by: Filter by user names that are allowed to start an instance of the
                             process definition.
        :param active: Whether to include only active process definitions.
        :param suspended: Whether to include only suspended process definitions.
        :param incident_id: Filter by incident id.
        :param incident_type: Filter by incident type.
        :param incident_message: Filter by the incident message.
        :param incident_message_like: Filter by a substring the incident message.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Whether to include only process definitions that belong to no
                                  tenant.
        :param include_without_tenant_id: Whether to include process definitions that belong to no
                                          tenant.
        :param version_tag: Filter by the version tag.
        :param version_tag_like: Filter by a substring of the version tag.
        :param without_version_tag: Whether to include only process definition without a version
                                    tag.
        :param startable_in_tasklist: Filter by process definition that are startable in tasklist.
        :param not_startable_in_tasklist: Filter by process definitions that are not startable in
                                          tasklist.
        :param startable_permission_check: Filter by process definitions that the user is allowed to
                                           start.
        """
        super().__init__(url=url + URL_SUFFIX + '/count')
        self.id_ = id_
        self.id_in = id_in
        self.name = name
        self.name_like = name_like
        self.deployment_id = deployment_id
        self.key = key
        self.key_like = key_like
        self.key_in = key_in
        self.category = category
        self.category_like = category_like
        self.version = version
        self.latest_version = latest_version
        self.resource_name = resource_name
        self.resource_name_like = resource_name_like
        self.startable_by = startable_by
        self.active = active
        self.suspended = suspended
        self.incident_id = incident_id
        self.incident_type = None
        if incident_type is not None:
            self.incident_type = pycamunda.incident.IncidentType(incident_type)
        self.incident_message = incident_message
        self.incident_message_like = incident_message_like
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.include_without_tenant_id = include_without_tenant_id
        self.version_tag = version_tag
        self.version_tag_like = version_tag_like
        self.without_version_tag = without_version_tag
        self.startable_in_tasklist = startable_in_tasklist
        self.not_startable_in_tasklist = not_startable_in_tasklist
        self.startable_permission_check = startable_permission_check

    def __call__(self, *args, **kwargs) -> int:
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return response.json()['count']


class GetList(pycamunda.base.CamundaRequest):

    id_ = QueryParameter('processDefinitionId')
    id_in = QueryParameter('processDefinitionIdIn')
    name = QueryParameter('name')
    name_like = QueryParameter('nameLike')
    deployment_id = QueryParameter('deploymentId')
    key = QueryParameter('key')
    key_in = QueryParameter('keysIn')
    key_like = QueryParameter('keyLike')
    category = QueryParameter('category')
    category_like = QueryParameter('categoryLike')
    version = QueryParameter('version')
    latest_version = QueryParameter('latestVersion', provide=pycamunda.base.value_is_true)
    resource_name = QueryParameter('resourceName')
    resource_name_like = QueryParameter('resourceNameLike')
    startable_by = QueryParameter('startableBy')
    active = QueryParameter('active', provide=pycamunda.base.value_is_true)
    suspended = QueryParameter('suspended', provide=pycamunda.base.value_is_true)
    incident_id = QueryParameter('incidentId')
    incident_type = QueryParameter('incidentType')
    incident_message = QueryParameter('incidentMessage')
    incident_message_like = QueryParameter('incidentMessageLike')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.base.value_is_true)
    include_without_tenant_id = QueryParameter(
        'includeProcessDefinitionsWithoutTenantId',
        provide = pycamunda.base.value_is_true
    )
    version_tag = QueryParameter('versionTag')
    version_tag_like = QueryParameter('versionTagLike')
    without_version_tag = QueryParameter('withoutVersionTag')
    startable_in_tasklist = QueryParameter('startableInTasklist')
    not_startable_in_tasklist = QueryParameter('notStartableInTasklist')
    startable_permission_check = QueryParameter(
        'startablePermissionCheck',
        mapping={True: 'true', False: 'false'}
    )
    sort_by = QueryParameter(
        'sortBy',
        mapping={
            'category': 'category',
            'key': 'key', 'id_': 'id',
            'name': 'name',
            'version': 'version',
            'deployment_id': 'deploymentId',
            'tenant_id': 'tenantId',
            'version_tag': 'versionTag'
        }
    )
    ascending = QueryParameter(
        'sortOrder',
        mapping={True: 'asc', False: 'desc'},
        provide=lambda self, obj, obj_type: vars(obj).get('sort_by', None) is not None
    )
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')

    def __init__(
        self,
        url: str,
        id_: str = None,
        id_in: typing.Iterable[str] = None,
        name: str = None,
        name_like: str = None,
        deployment_id: str = None,
        key: str = None,
        key_in: typing.Iterable[str] = None,
        key_like: str = None,
        category: str = None,
        category_like: str = None,
        version: str = None,
        latest_version: bool = False,
        resource_name: str = None,
        resource_name_like: str = None,
        startable_by: str = None,
        active: bool = False,
        suspended: bool = False,
        incident_id: str = None,
        incident_type: typing.Union[str, pycamunda.incident.IncidentType] = None,
        incident_message: str = None,
        incident_message_like: str = None,
        tenant_id_in: typing.Iterable[str] = None,
        without_tenant_id: bool = False,
        include_without_tenant_id: bool = False,
        version_tag: str = None,
        version_tag_like: str = None,
        without_version_tag: bool = None,
        startable_in_tasklist: bool = None,
        startable_permission_check: bool = None,
        not_startable_in_tasklist: bool = None,
        sort_by: str = None,
        ascending: bool = True,
        first_result: int = None,
        max_results: int = None
    ):
        """Query for a list of process definitions using a list of parameters. The size of the
        result set can be retrieved by using the Get List Count method.

        :param url: Camunda Rest engine URL.
        :param id_: Filter by id.
        :param id_in: Filter whether the id is one of multiple ones.
        :param name: Filter by name.
        :param name_like: Filter by a substring of the name.
        :param deployment_id: Filter by deployment id.
        :param key: Key of the process definition.
        :param key_in: Filter whether the key is one of multiple ones.
        :param key_like: Filter by a substring of the key.
        :param category: Filter by category.
        :param category_like: Filter by a substring of the category.
        :param version: Filter by version.
        :param latest_version: Whether to include only the latest versions.
        :param resource_name: Filter by resource name.
        :param resource_name_like: Filter by a substring of the resource name.
        :param startable_by: Filter by user names that are allowed to start an instance of the
                             process definition.
        :param active: Whether to include only active process definitions.
        :param suspended: Whether to include only suspended process definitions.
        :param incident_id: Filter by incident id.
        :param incident_type: Filter by incident type.
        :param incident_message: Filter by the incident message.
        :param incident_message_like: Filter by a substring the incident message.
        :param tenant_id_in: Filter whether the tenant id is one of multiple ones.
        :param without_tenant_id: Whether to include only process definitions that belong to no
                                  tenant.
        :param include_without_tenant_id: Whether to include process definitions that belong to no
                                          tenant.
        :param version_tag: Filter by the version tag.
        :param version_tag_like: Filter by a substring of the version tag.
        :param without_version_tag: Whether to include only process definition without a version
                                    tag.
        :param startable_in_tasklist: Filter by process definition that are startable in tasklist.
        :param not_startable_in_tasklist: Filter by process definitions that are not startable in
                                          tasklist.
        :param startable_permission_check: Filter by process definitions that the user is allowed to
                                           start.
        :param sort_by: Sort the results by 'category', 'key', 'id_', 'name', 'version',
                        'deployment_id', 'tenant_id' or `version_tag`. Sorting by 'version_tag' is
                        string-based.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.id_ = id_
        self.id_in = id_in
        self.name = name
        self.name_like = name_like
        self.deployment_id = deployment_id
        self.key = key
        self.key_like = key_like
        self.key_in = key_in
        self.category = category
        self.category_like = category_like
        self.version = version
        self.latest_version = latest_version
        self.resource_name = resource_name
        self.resource_name_like = resource_name_like
        self.startable_by = startable_by
        self.active = active
        self.suspended = suspended
        self.incident_id = incident_id
        self.incident_type = None
        if incident_type is not None:
            self.incident_type = pycamunda.incident.IncidentType(incident_type)
        self.incident_message = incident_message
        self.incident_message_like = incident_message_like
        self.tenant_id_in = tenant_id_in
        self.without_tenant_id = without_tenant_id
        self.include_without_tenant_id = include_without_tenant_id
        self.version_tag = version_tag
        self.version_tag_like = version_tag_like
        self.without_version_tag = without_version_tag
        self.startable_in_tasklist = startable_in_tasklist
        self.not_startable_in_tasklist = not_startable_in_tasklist
        self.startable_permission_check = startable_permission_check
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results

    def __call__(self, *args, **kwargs) -> typing.Tuple[ProcessDefinition]:
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return tuple(ProcessDefinition.load(definition_json) for definition_json in response.json())


class GetProcessInstanceStats(pycamunda.base.CamundaRequest):

    failed_jobs = QueryParameter('failedJobs')
    incidents = QueryParameter('incidents', provide=pycamunda.base.value_is_true)
    root_incidents = QueryParameter('rootIncidents', provide=pycamunda.base.value_is_true)
    incidents_for_type = QueryParameter('incidentsForType')

    def __init__(
        self,
        url: str,
        failed_jobs: bool = False,
        incidents: bool = False,
        root_incidents: bool = False,
        incidents_for_type: typing.Union[str, pycamunda.incident.IncidentType] = None
    ):
        """Get runtime statistics grouped by process definition. Does not include historic data.

        :param url: Camunda Rest engine URL.
        :param failed_jobs: Whether the number of failed jobs should be included.
        :param incidents: Whether to include the number of incidents.
        :param root_incidents: Whether to include the corresponding number of root incidents for
                               each incident type.
        :param incidents_for_type: Include only incidents of a specific type.
        """
        if sum((incidents, root_incidents, incidents_for_type is not None)) > 1:
            raise pycamunda.PyCamundaException(
                'Either \'incidents\', \'root_incidents\' or \'incidents_for_type\' can be '
                'provided, not multiple of them.'
            )
        super().__init__(url=url + URL_SUFFIX + '/statistics')
        self.failed_jobs = failed_jobs
        self.incidents = incidents
        self.root_incidents = root_incidents
        self.incidents_for_type = None
        if incidents_for_type is not None:
            self.incidents_for_type = pycamunda.incident.IncidentType(incidents_for_type)

    def __call__(self, *args, **kwargs) -> typing.Tuple[ProcessInstanceStats]:
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return tuple(ProcessInstanceStats.load(stats_json) for stats_json in response.json())


class GetXML(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')

    def __init__(self, url: str, id_: str = None, key: str = None, tenant_id: str = None):
        """Get the BPMN xml diagram of a process definition.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process definition.
        :param key: Key of the process definition.
        :param tenant_id: Id of the tenant the process definition belongs to.
        """
        super().__init__(url=url + URL_SUFFIX + '/{path}/xml')
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id

    @property
    def url(self):
        if self.id_ is not None:
            return self._url.format(path=self.id_)
        if self.tenant_id is not None:
            return self._url.format(path=f'key/{self.key}/tenant-id/{self.tenant_id}')
        return self._url.format(path=f'key/{self.key}')

    def __call__(self, *args, **kwargs) -> str:
        """Send the request."""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return response.json()['bpmn20Xml']


class Get(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')

    def __init__(self, url: str, id_: str = None, key: str = None, tenant_id: str = None):
        """Get a process definition.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process definition.
        :param key: Key of the process definition.
        :param tenant_id: Id of the tenant the process definition belongs to.

        """
        super().__init__(url=url + URL_SUFFIX + '/{path}')
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id

    @property
    def url(self):
        if self.id_ is not None:
            return self._url.format(path=self.id_)
        if self.tenant_id is not None:
            return self._url.format(path=f'key/{self.key}/tenant-id/{self.tenant_id}')
        return self._url.format(path=f'key/{self.key}')

    def __call__(self, *args, **kwargs) -> ProcessDefinition:
        """Send the request."""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return ProcessDefinition.load(response.json())


class StartInstance(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')

    variables = BodyParameter('variables')
    business_key = BodyParameter('businessKey')
    case_instance_key = BodyParameter('caseInstanceId')
    start_instructions = BodyParameter('startInstructions')
    skip_custom_listeners = BodyParameter('skipCustomListeners')
    skip_io_mappings = BodyParameter('skipIoMappings')
    with_variables_in_return = BodyParameter('withVariablesInReturn')

    def __init__(
        self,
        url: str,
        id_: str = None,
        key: str = None,
        tenant_id: str = None,
        business_key: str = None,
        case_instance_id: str = None,
        skip_custom_listeners: bool = False,
        skip_io_mappings: bool = False,
        with_variables_in_return: bool = False
    ):
        """Start a process instance of a specific process definition.

        The process definition can be chosen by providing either the id or the key of the process
        definition. If chosen by key the latest version of that process definition is used. In case
        the key of the process definition is provided, the tenant id can be provided aswell.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process definition.
        :param key: Key of the process definition.
        :param tenant_id: Id of the tenant the process definition belongs to.
        :param business_key: The business key to initialize the process instance with.
        :param case_instance_id: The case instance id to initialize the process instance with.
        :param skip_custom_listeners: Whether to skip custom listeners and notify only builtin ones.
        :param skip_io_mappings: Whether to skip input/output mappings.
        :param with_variables_in_return: Whether the variable that were used by the process instance
                                         during execution should be returned.
        """
        if id_ is not None and key is not None:
            raise pycamunda.PyCamundaException('Either `id_ or `key` can be provided, not both.')
        if tenant_id is not None and key is None:
            raise pycamunda.PyCamundaException(
                'If `tenant_id is provided `key also has to be provided.'
            )
        super().__init__(url=url + URL_SUFFIX + '/{path}/start')
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id
        self.business_key = business_key
        self.case_instance_key = case_instance_id
        self.skip_custom_listeners = skip_custom_listeners
        self.skip_io_mappings = skip_io_mappings
        self.with_variables_in_return = with_variables_in_return

        self.variables = {}
        self.start_instructions = []

    @property
    def url(self):
        if self.id_ is not None:
            return self._url.format(path=self.id_)
        if self.tenant_id is not None:
            return self._url.format(path=f'key/{self.key}/tenant-id/{self.tenant_id}')
        return self._url.format(path=f'key/{self.key}')

    def add_variable(
        self, name: str, value: typing.Any, type_: str = None, value_info: str = None
    ) -> None:
        """Add a variable to initialize the process instance with.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable.
        :param value_info: Additional information regarding the value type.
        """
        self.variables[name] = {'value': value, 'type': type_, 'valueInfo': value_info}

    def _add_start_instruction(
        self,
        type_: typing.Union[str, pycamunda.instruction.InstructionType],
        activity_id: str = None,
        transition_id: str = None,
        variables: typing.Mapping[str, pycamunda.variable.Variable] = None
    ) -> None:
        """Add an instruction that specifies at which activities the process instance is started.

        :param type_: Type of the instruction. Possible values are
                          - startBeforeActivity
                          - startAfterActivity
                          - startTransition
        :param activity_id: Id of the activity in case `type_` is `startBeforeActivity` or
                            `startAfterActivity.
        :param transition_id: Id of the sequence flow to start.
        :param variables: Mapping from names to the corresponding variables.
        :return:
        """
        instruction = {'type': pycamunda.instruction.InstructionType(type_).value}
        if activity_id is not None:
            instruction['activityId'] = activity_id
        if transition_id is not None:
            instruction['transitionId'] = transition_id
        if variables is not None:
            instruction['variables'] = {
                name: dataclasses.asdict(var) for name, var in variables.items()
            }

        self.start_instructions.append(instruction)

    def add_start_before_activity_instruction(
        self,
        id_: str,
        variables: typing.Mapping[str, pycamunda.variable.Variable] = None
    ) -> None:
        """Add an instruction to start execution before a given activity is entered.

        :param id_: Id of the activity.
        :param variables: Mapping from names to the corresponding variables.
        """
        self._add_start_instruction(
            type_=pycamunda.instruction.InstructionType.start_before_activity,
            activity_id=id_,
            variables=variables
        )

    def add_start_after_activity_instruction(
        self,
        id_: str,
        variables: typing.Mapping[str, pycamunda.variable.Variable] = None
    ) -> None:
        """Add an instruction to start execution at the single outgoing sequence flow of an
        activity.

        :param id_: Id of the activity.
        :param variables: Mapping from names to the corresponding variables.
        """
        self._add_start_instruction(
            type_=pycamunda.instruction.InstructionType.start_after_activity,
            activity_id=id_,
            variables=variables
        )

    def add_start_transition_instruction(
        self,
        id_: str,
        variables: typing.Mapping[str, pycamunda.variable.Variable] = None
    ) -> None:
        """Add an instruction to start execution at the single outgoing sequence flow of an
        activity.

        :param id_: Id of the sequence flow to start.
        :param variables: Mapping from names to the corresponding variables.
        """
        self._add_start_instruction(
            type_=pycamunda.instruction.InstructionType.start_transition,
            transition_id=id_,
            variables=variables
        )

    def __call__(self, *args, **kwargs) -> pycamunda.processinst.ProcessInstance:
        """Send the request."""
        params = self.body_parameters()
        try:
            response = requests.post(self.url, json=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        return pycamunda.processinst.ProcessInstance.load(response.json())


class _ActivateSuspend(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')

    suspended = BodyParameter('suspended')
    include_process_instances = BodyParameter('includeProcessInstances')
    execution_datetime = BodyParameter('executionDate')

    def __init__(
        self,
        url: str,
        suspended: bool,
        id_: str = None,
        key: str = None,
        tenant_id: str = None,
        include_process_instances: bool = None,
        execution_datetime: dt.datetime = None
    ):
        """Activate or Suspend a process definition.

        :param url: Camunda Rest engine URL.
        :param suspended: Whether to suspend or activate the process definition.
        :param id_: Id of the process definition.
        :param key: Key of the process definition.
        :param tenant_id: Id of the tenant the process definition belongs to.
        :param include_process_instances: Whether to cascade the action to process instances.
        :param execution_datetime: When to execute the action. If 'None' the action is immediately.
        """
        super().__init__(url=url + URL_SUFFIX + '/{path}/suspended')
        self.suspended = suspended
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id
        self.include_process_instances = include_process_instances
        self.execution_datetime = execution_datetime

    @property
    def url(self):
        if self.id_ is not None:
            return self._url.format(path=self.id_)
        if self.tenant_id is not None:
            return self._url.format(path=f'key/{self.key}/tenant-id/{self.tenant_id}')
        return self._url.format(path=f'key/{self.key}')

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        params = self.body_parameters()
        try:
            response = requests.put(self.url, json=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)


class Activate(_ActivateSuspend):

    def __init__(
        self,
        url: str,
        id_: str = None,
        key: str = None,
        tenant_id: str = None,
        include_process_instances: bool = None,
        execution_datetime: dt.datetime = None
    ):
        """Activate a process definition.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process definition.
        :param key: Key of the process definition.
        :param tenant_id: Id of the tenant the process definition belongs to.
        :param include_process_instances: Whether to cascade the action to process instances.
        :param execution_datetime: When to execute the action. If 'None' the action is immediately.
        """
        super().__init__(
            url=url,
            suspended=False,
            id_=id_,
            key=key,
            tenant_id=tenant_id,
            include_process_instances=include_process_instances,
            execution_datetime=execution_datetime
        )


class Suspend(_ActivateSuspend):

    def __init__(
            self,
            url: str,
            id_: str = None,
            key: str = None,
            tenant_id: str = None,
            include_process_instances: bool = None,
            execution_datetime: dt.datetime = None
    ):
        """Suspend a process definition.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process definition.
        :param key: Key of the process definition.
        :param tenant_id: Id of the tenant the process definition belongs to.
        :param include_process_instances: Whether to cascade the action to process instances.
        :param execution_datetime: When to execute the action. If 'None' the action is immediately.
        """
        super().__init__(
            url=url,
            suspended=True,
            id_=id_,
            key=key,
            tenant_id=tenant_id,
            include_process_instances=include_process_instances,
            execution_datetime=execution_datetime
        )


class UpdateHistoryTimeToLive(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')

    history_time_to_live = BodyParameter(
        'historyTimeToLive',
        validate=lambda val: val is None or val >= 0
    )

    def __init__(
        self,
        url: str,
        history_time_to_live: int,
        id_: str = None,
        key: str = None,
        tenant_id: str = None
    ):
        """Update the history time to live of a process definition.

        :param url: Camunda Rest engine URL.
        :param history_time_to_live: New history time to live. Can be set to 'None'.
        :param id_: Id of the process definition.
        :param key: Key of the process definition.
        :param tenant_id: Id of the tenant the process definition belongs to.
        """
        super().__init__(url=url + URL_SUFFIX + '/{path}/history-time-to-live')
        self.history_time_to_live = history_time_to_live
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id

    @property
    def url(self):
        if self.id_ is not None:
            return self._url.format(path=self.id_)
        if self.tenant_id is not None:
            return self._url.format(path=f'key/{self.key}/tenant-id/{self.tenant_id}')
        return self._url.format(path=f'key/{self.key}')

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        params = self.body_parameters()
        try:
            response = requests.put(self.url, json=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)


class Delete(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')

    cascade = QueryParameter('cascade')
    skip_custom_listeners = QueryParameter('skipCustomListeners')
    skip_io_mappings = QueryParameter('skipIoMappings')

    def __init__(
        self,
        url: str,
        id_: str = None,
        key: str = None,
        tenant_id: str = None,
        cascade: bool = False,
        skip_custom_listeners: bool = False,
        skip_io_mappings: bool = False
    ):
        """Delete a process definition.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process definition.
        :param key: Key of the process definition.
        :param tenant_id: Id of the tenant the process definition belongs to.
        :param cascade: Whether to cascade the deletion to process instances of the definition.
        :param skip_custom_listeners: Whether to skip custom listeners and notify only builtin ones.
        :param skip_io_mappings: Whether to skip input/output mappings.
        """
        super().__init__(url=url + URL_SUFFIX + '/{path}')
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id
        self.cascade = cascade
        self.skip_custom_listeners = skip_custom_listeners
        self.skip_io_mappings = skip_io_mappings

    @property
    def url(self):
        if self.id_ is not None:
            return self._url.format(path=self.id_)
        if self.tenant_id is not None:
            return self._url.format(path=f'key/{self.key}/tenant-id/{self.tenant_id}')
        return self._url.format(path=f'key/{self.key}')

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        params = self.query_parameters()
        try:
            response = requests.delete(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)


class RestartProcessInstance(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')
    process_instance_ids = BodyParameter('processInstanceIds')
    historic_process_instance_query = BodyParameterContainer('historicProcessInstanceQuery')  # TODO create method to add this parameter
    skip_custom_listeners = BodyParameter('skipCustomListeners')
    skip_io_mappings = BodyParameter('skipIoMappings')
    initial_variables = BodyParameter('initialVariables')
    without_business_key = BodyParameter('withoutBusinessKey')
    instructions = BodyParameter('instructions')

    def __init__(
        self,
        url: str,
        id_: str,
        process_instance_ids: typing.Iterable[str],
        async_: bool = False,
        skip_custom_listeners: bool = False,
        skip_io_mappings: bool = False,
        initial_variables: bool = True,
        without_business_key: bool = False
    ):
        """Restart process instances of a specific process definition.

        :param url: Camunda Rest engine url.
        :param id_: Id of the process definition.
        :param process_instance_ids: Ids of the process instances to restart.
        :param async_: Whether to restart the processes asynchronously.
        :param skip_custom_listeners: Whether to skip custom listeners and notify only builtin ones.
        :param skip_io_mappings: Whether to skip input/output mappings.
        :param initial_variables: Whether to set the initial set of variables.
        :param without_business_key: Whether not to add the business key of the process instance.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/restart')
        self.id_ = id_
        self.process_instance_ids = process_instance_ids
        self.async_ = async_
        self.skip_custom_listeners = skip_custom_listeners
        self.skip_io_mappings = skip_io_mappings
        self.initial_variables = initial_variables
        self.without_business_key = without_business_key

        self.instructions = []

    @property
    def url(self) -> str:
        return super().url + ('-async' if self.async_ else '')

    def _add_instruction(
        self,
        type_: typing.Union[str, pycamunda.instruction.InstructionType],
        activity_id: str = None,
        transition_id: str = None
    ) -> None:
        """Add an instruction that specifies at which activities the process instance is started.

        :param type_: Type of the instruction. Possible values are
                          - startBeforeActivity
                          - startAfterActivity
                          - startTransition
        :param activity_id: Id of the activity in case `type_` is `startBeforeActivity` or
                            `startAfterActivity.
        :param transition_id: Id of the sequence flow to start.
        """
        instruction = {'type': pycamunda.instruction.InstructionType(type_).value}
        if activity_id is not None:
            instruction['activityId'] = activity_id
        if transition_id is not None:
            instruction['transitionId'] = transition_id

        self.instructions.append(instruction)

    def add_before_activity_instruction(self, id_: str) -> None:
        """Add an instruction to start execution before a given activity is entered.

        :param id_: Id of the activity.
        """
        self._add_instruction(
            type_=pycamunda.instruction.InstructionType.start_before_activity,
            activity_id=id_
        )

    def add_after_activity_instruction(self, id_: str) -> None:
        """Add an instruction to start execution at the single outgoing sequence flow of an
        activity.

        :param id_: Id of the activity.
        """
        self._add_instruction(
            type_=pycamunda.instruction.InstructionType.start_after_activity,
            activity_id=id_
        )

    def add_transition_instruction(self, id_: str) -> None:
        """Add an instruction to start execution at the single outgoing sequence flow of an
        activity.

        :param id_: Id of the sequence flow to start.
        """
        self._add_instruction(
            type_=pycamunda.instruction.InstructionType.start_transition,
            transition_id=id_
        )

    def __call__(self, *args, **kwargs) -> typing.Optional[pycamunda.batch.Batch]:
        """Send the request."""
        params = self.body_parameters()
        try:
            response = requests.post(self.url, json=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            pycamunda.base._raise_for_status(response)

        if self.async_:
            return pycamunda.batch.Batch.load(response.json())
