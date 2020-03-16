# -*- coding: utf-8 -*-

import enum
import typing
import dataclasses

import requests

import pycamunda.request
import pycamunda.variable
import pycamunda.process_instance
from pycamunda.request import PathParameter, QueryParameter, BodyParameter, BodyParameterContainer


URL_SUFFIX = '/process-definition'


class _StartInstancePathParameter(PathParameter):

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


class InstructionType(enum.Enum):

    start_before_activity = 'startBeforeActivity'
    start_after_activity = 'startAfterActivity'
    start_transition = 'startTransition'


class StartInstance(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')
    key = PathParameter('key')
    tenant_id = PathParameter('tenant-id')
    path = _StartInstancePathParameter('path', id_, key, tenant_id)

    variables = BodyParameter('variables')
    business_key = BodyParameter('businessKey')
    case_instance_key = BodyParameter('caseInstanceId')
    start_instructions = BodyParameter('startInstructions')  # TODO
    skip_custom_listeners = BodyParameter('skipCustomListeners')  # TODO
    skip_io_mappings = BodyParameter('skipIoMappings')  # TODO
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
            variables: typing.Mapping[str, pycamunda.variable.Variable] = None
    ):
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
        variables: typing.Mapping[str, pycamunda.variable.Variable] = None
    ):
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
        variables: typing.Mapping[str, pycamunda.variable.Variable] = None
    ):
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
        variables: typing.Mapping[str, pycamunda.variable.Variable] = None
    ):
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
        print(params)
        try:
            response = requests.post(self.url, json=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return pycamunda.process_instance.ProcessInstance.load(response.json())
