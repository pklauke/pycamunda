# -*- coding: utf-8 -*-

"""This module provides access to the process definition REST api of Camunda."""

import enum
import typing
import dataclasses

import requests

import pycamunda.request
import pycamunda.variable
import pycamunda.process_instance
from pycamunda.request import PathParameter, QueryParameter, BodyParameter, BodyParameterContainer


URL_SUFFIX = '/process-definition'


@dataclasses.dataclass
class ProcessDefinition:
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
    def load(cls, data):
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


class _ProcessDefinitionPathParameter(PathParameter):

    def __init__(self, key, id_parameter, key_parameter, tenant_id_parameter):
        super().__init__(key=key)
        self.id_parameter = id_parameter
        self.key_parameter = key_parameter
        self.tenant_id_parameter = tenant_id_parameter

    def __call__(self, *args, **kwargs):
        if self.id_parameter() is not None:
            return self.id_parameter()
        if self.tenant_id_parameter() is not None:
            return f'key/{self.key_parameter()}/tenant-id/{self.tenant_id_parameter()}'
        return f'key/{self.key_parameter()}'


class IncidentType(enum.Enum):
    failed_job = 'failedJob'
    failed_external_task = 'failedExternalTask'


@dataclasses.dataclass
class Incident:
    incident_type: IncidentType
    incident_count: int

    @classmethod
    def load(cls, data):
        return cls(
            incident_type=IncidentType(data['incidentType']),
            incident_count=data['incidentCount']
        )


@dataclasses.dataclass
class ActivityStatistics:
    id_: str
    instances: int
    failed_jobs: int
    incidents: typing.Iterable[Incident]

    @classmethod
    def load(cls, data):
        return cls(
            id_=data['id'],
            instances=data['instances'],
            failed_jobs=data['failedJobs'],
            incidents=tuple(Incident.load(incident_data) for incident_data in data['incidents'])
        )


class GetActivityInstanceStatistics(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')
    path = _ProcessDefinitionPathParameter('path', id_, key, tenant_id)

    failed_jobs = QueryParameter('failedJobs')
    incidents = QueryParameter('incidents')
    incidents_for_type = QueryParameter('incidentsForType')

    def __init__(self, url, id_=None, key=None, tenant_id=None, failed_jobs=None, incidents=False,
                 incidents_for_type=None):
        """Get runtime statistics for a process definition. Does not include historic data.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process definition.
        :param key: Key of the process definition.
        :param tenant_id: Id of the tenant the process definition belongs to.
        :param failed_jobs: Whether the number of failed jobs should be included.
        :param incidents: Whether to include the number of incidents.
        :param incidents_for_type: Include only incidents of a specific type.
        """
        super().__init__(url + URL_SUFFIX + '/{path}/statistics')
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id
        self.failed_jobs = failed_jobs
        self.incidents = incidents
        self.incidents_for_type = incidents_for_type

    def send(self):
        """Send the request"""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return tuple(ActivityStatistics.load(activity_json) for activity_json in response.json())


class GetProcessDiagram(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')
    path = _ProcessDefinitionPathParameter('path', id_, key, tenant_id)

    def __init__(self, url, id_=None, key=None, tenant_id=None):
        """Get the diagram of a process definition.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the process definition.
        :param key: Key of the process definition.
        """
        super().__init__(url + URL_SUFFIX + '/{path}/diagram')
        self.id_ = id_
        self.key = key
        self.tenant_id = tenant_id

    def send(self):
        """Send the request"""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return response.content


class Count(pycamunda.request.CamundaRequest):

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
    latest_version = QueryParameter('latestVersion', provide=pycamunda.request.value_is_true)
    resource_name = QueryParameter('resourceName')
    resource_name_like = QueryParameter('resourceNameLike')
    startable_by = QueryParameter('startableBy')
    active = QueryParameter('active', provide=pycamunda.request.value_is_true)
    suspended = QueryParameter('suspended', provide=pycamunda.request.value_is_true)
    incident_id = QueryParameter('incidentId')
    incident_type = QueryParameter('incidentType')
    incident_message = QueryParameter('incidentMessage')
    incident_message_like = QueryParameter('incidentMessageLike')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.request.value_is_true)
    include_without_tenant_id = QueryParameter(
        'includeProcessDefinitionsWithoutTenantId',
        provide = pycamunda.request.value_is_true
    )
    version_tag = QueryParameter('versionTag')
    version_tag_like = QueryParameter('versionTagLike')
    without_version_tag = QueryParameter('withoutVersionTag')
    startable_in_tasklist = QueryParameter('startableInTasklist')
    not_startable_in_tasklist = QueryParameter('notStartableInTasklist')
    startable_permission_check = QueryParameter('startablePermissionCheck')
    sort_by = QueryParameter(
        'sortBy',
        mapping={'category': 'category', 'key': 'key', 'id_': 'id', 'name': 'name',
                 'version': 'version', 'deployment_id': 'deploymentId', 'tenant_id': 'tenantId',
                 'version_tag': 'versionTag'}
    )
    ascending = QueryParameter('sortOrder', mapping={True: 'asc', False: 'desc'},
                               provide=lambda self, obj, obj_type: 'sort_by' in vars(self))
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')

    def __init__(self, url, id_=None, id_in=None, name=None, name_like=None, deployment_id=None,
                 key=None, key_in=None, key_like=None, category=None, category_like=None,
                 version=None, latest_version=False, resource_name=None, resource_name_like=None,
                 startable_by=None, active=False, suspended=False, incident_id=None,
                 incident_type=None, incident_message=None, incident_message_like=None,
                 tenant_id_in=None, without_tenant_id=False, include_without_tenant_id=False,
                 version_tag=None, version_tag_like=None, without_version_tag=None,
                 startable_in_tasklist=None, not_startable_in_tasklist=None,
                 startable_permission_check=None, sort_by=None, ascending=True, first_result=None,
                 max_results=None):
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
        :param sort_by: Sort the results by 'category', 'key', 'id_', 'name', 'version',
                        'deployment_id', 'tenant_id' or `version_tag`. Sorting by 'version_tag' is
                        string-based.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url + URL_SUFFIX + '/count')
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
        self.incident_type = incident_type  # TODO handle in case IncidentType is given
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

    def send(self):
        """Send the request"""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return response.json()['count']


class GetList(pycamunda.request.CamundaRequest):

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
    latest_version = QueryParameter('latestVersion', provide=pycamunda.request.value_is_true)
    resource_name = QueryParameter('resourceName')
    resource_name_like = QueryParameter('resourceNameLike')
    startable_by = QueryParameter('startableBy')
    active = QueryParameter('active', provide=pycamunda.request.value_is_true)
    suspended = QueryParameter('suspended', provide=pycamunda.request.value_is_true)
    incident_id = QueryParameter('incidentId')
    incident_type = QueryParameter('incidentType')
    incident_message = QueryParameter('incidentMessage')
    incident_message_like = QueryParameter('incidentMessageLike')
    tenant_id_in = QueryParameter('tenantIdIn')
    without_tenant_id = QueryParameter('withoutTenantId', provide=pycamunda.request.value_is_true)
    include_without_tenant_id = QueryParameter(
        'includeProcessDefinitionsWithoutTenantId',
        provide = pycamunda.request.value_is_true
    )
    version_tag = QueryParameter('versionTag')
    version_tag_like = QueryParameter('versionTagLike')
    without_version_tag = QueryParameter('withoutVersionTag')
    startable_in_tasklist = QueryParameter('startableInTasklist')
    not_startable_in_tasklist = QueryParameter('notStartableInTasklist')
    startable_permission_check = QueryParameter('startablePermissionCheck')
    sort_by = QueryParameter(
        'sortBy',
        mapping={'category': 'category', 'key': 'key', 'id_': 'id', 'name': 'name',
                 'version': 'version', 'deployment_id': 'deploymentId', 'tenant_id': 'tenantId',
                 'version_tag': 'versionTag'}
    )
    ascending = QueryParameter('sortOrder', mapping={True: 'asc', False: 'desc'},
                               provide=lambda self, obj, obj_type: 'sort_by' in vars(self))
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')

    def __init__(self, url, id_=None, id_in=None, name=None, name_like=None, deployment_id=None,
                 key=None, key_in=None, key_like=None, category=None, category_like=None,
                 version=None, latest_version=False, resource_name=None, resource_name_like=None,
                 startable_by=None, active=False, suspended=False, incident_id=None,
                 incident_type=None, incident_message=None, incident_message_like=None,
                 tenant_id_in=None, without_tenant_id=False, include_without_tenant_id=False,
                 version_tag=None, version_tag_like=None, without_version_tag=None,
                 startable_in_tasklist=None, not_startable_in_tasklist=None,
                 startable_permission_check=None, sort_by=None, ascending=True, first_result=None,
                 max_results=None):
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
        super().__init__(url + URL_SUFFIX)
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
        self.incident_type = incident_type  # TODO handle in case IncidentType is given
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

    def send(self):
        """Send the request"""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return tuple(ProcessDefinition.load(definition_json) for definition_json in response.json())


class InstructionType(enum.Enum):
    start_before_activity = 'startBeforeActivity'
    start_after_activity = 'startAfterActivity'
    start_transition = 'startTransition'


class StartInstance(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')
    path = _ProcessDefinitionPathParameter('path', id_, key, tenant_id)

    variables = BodyParameter('variables')
    business_key = BodyParameter('businessKey')
    case_instance_key = BodyParameter('caseInstanceId')
    start_instructions = BodyParameter('startInstructions')
    skip_custom_listeners = BodyParameter('skipCustomListeners')
    skip_io_mappings = BodyParameter('skipIoMappings')
    with_variables_in_return = BodyParameter('withVariablesInReturn')

    def __init__(self, url, id_=None, key=None, tenant_id=None, business_key=None,
                 case_instance_id=None, skip_custom_listeners=False, skip_io_mappings=False,
                 with_variables_in_return=False):
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
        :param skip_custom_listeners: Skip execution listener invocation for activities that are
                                      started or ended as part of this request.
        :param skip_io_mappings: Skip execution of input/output variable mappings for activities
                                 that are started or ended as part of this request.
        :param with_variables_in_return: Whether the variable that were used by the process instance
                                         during execution should be returned.
        """
        if id_ is not None and key is not None:
            raise pycamunda.PyCamundaInvalidInput('Either `id_ or `key` can be provided, not both.')
        if tenant_id is not None and key is None:
            raise pycamunda.PyCamundaInvalidInput(
                'If `tenant_id is provided `key also has to be provided.'
            )
        super().__init__(url + URL_SUFFIX + '/{path}/start')
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

    def add_variable(self, name, value, type_=None, value_info=None):
        """Add a variable to initialize the process instance with.

        :param name: Name of the variable.
        :param value: Value of the variable.
        :param type_: Value type of the variable.
        :param value_info: Additional information regarding the value type.
        """
        self.variables[name] = {'value': value, 'type': type_, 'valueInfo': value_info}

        return self

    def _add_start_instruction(
            self,
            type_: typing.Union[str, InstructionType],
            activity_id: str = None,
            transition_id: str = None,
            variables: typing.Mapping[str, pycamunda.variable.Variable] = None):
        """Add an instruction that specify at which activities the process instance is started.

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
        instruction = {'type': InstructionType(type_).value}
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
            activity_id,
            variables: typing.Mapping[str, pycamunda.variable.Variable] = None):
        """Add an instruction to start execution before a given activity is entered.

        :param activity_id: Id of the activity.
        :param variables: Mapping from names to the corresponding variables.
        """
        self._add_start_instruction(
            type_=InstructionType.start_before_activity,
            activity_id=activity_id,
            variables=variables
        )

        return self

    def add_start_after_activity_instruction(
            self,
            activity_id,
            variables: typing.Mapping[str, pycamunda.variable.Variable] = None):
        """Add an instruction to start execution at the single outgoing sequence flow of an
        activity.

        :param activity_id: Id of the activity.
        :param variables: Mapping from names to the corresponding variables.
        """
        self._add_start_instruction(
            type_=InstructionType.start_after_activity,
            activity_id=activity_id,
            variables=variables
        )

        return self

    def add_start_transition_instruction(
            self,
            transition_id,
            variables: typing.Mapping[str, pycamunda.variable.Variable] = None):
        """Add an instruction to start execution at the single outgoing sequence flow of an
        activity.

        :param transition_id: Id of the sequence flow to start.
        :param variables: Mapping from names to the corresponding variables.
        """
        self._add_start_instruction(
            type_=InstructionType.start_transition,
            transition_id=transition_id,
            variables=variables
        )

        return self

    def send(self):
        """Send the request"""
        params = self.body_parameters()
        try:
            response = requests.post(self.url, json=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return pycamunda.process_instance.ProcessInstance.load(response.json())
