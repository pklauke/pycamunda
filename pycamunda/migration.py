# -*- coding: utf-8 -*-

"""This module provides access to the migration REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing

import pycamunda.base
import pycamunda.batch
from pycamunda.request import BodyParameter

URL_SUFFIX = '/migration'


__all__ = ['Generate', 'Validate', 'Execute']


@dataclasses.dataclass
class MigrationInstruction:
    """Data class of migration instruction as returned by the REST api of Camunda."""
    source_activity_ids: typing.Tuple[str]
    target_activity_ids: typing.Tuple[str]
    update_event_trigger: bool

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> MigrationInstruction:
        return cls(
            source_activity_ids=data['sourceActivityIds'],
            target_activity_ids=data['targetActivityIds'],
            update_event_trigger=data['updateEventTrigger']
        )


@dataclasses.dataclass
class MigrationPlan:
    """Data class of migration plan as returned by the REST api of Camunda."""
    source_process_definition_id: str
    target_process_definition_id: str
    instructions: typing.Tuple[MigrationInstruction]

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> MigrationPlan:
        return cls(
            source_process_definition_id=data['sourceProcessDefinitionId'],
            target_process_definition_id=data['targetProcessDefinitionId'],
            instructions=tuple(
                MigrationInstruction.load(instruction_json)
                for instruction_json in data['instructions']
            )
        )


@dataclasses.dataclass
class InstructionReport:
    """Data class of instruction report as returned by the Camunda REST api."""
    instruction: MigrationInstruction
    failures: typing.Tuple[str]

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> InstructionReport:
        return cls(
            instruction=MigrationInstruction.load(data=data['instruction']),
            failures=tuple(failure_json for failure_json in data['failures'])
        )


class Generate(pycamunda.base.CamundaRequest):

    source_process_definition_id = BodyParameter('sourceProcessDefinitionId')
    target_process_definition_id = BodyParameter('targetProcessDefinitionId')
    update_event_triggers = BodyParameter('updateEventTriggers')

    def __init__(
        self,
        url: str,
        source_process_definition_id: str,
        target_process_definition_id: str,
        update_event_triggers: bool = False
    ):
        """Generates a migration plan for 2 process definitions. The generated plan contains
        instructions that map equal activities between the process definitions.

        :param url: Camunda Rest engine URL.
        :param source_process_definition_id: Id of the source process definition for the migration.
        :param target_process_definition_id: Id of the target process definition for the migration.
        :param update_event_triggers: Whether instructions between events should be configured to
                                      update the event triggers.
        """
        super().__init__(url=url + URL_SUFFIX + '/generate')
        self.source_process_definition_id = source_process_definition_id
        self.target_process_definition_id = target_process_definition_id
        self.update_event_triggers = update_event_triggers

    def __call__(self, *args, **kwargs) -> MigrationPlan:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)

        return MigrationPlan.load(data=response.json())


class Validate(pycamunda.base.CamundaRequest):

    source_process_definition_id = BodyParameter('sourceProcessDefinitionId')
    target_process_definition_id = BodyParameter('targetProcessDefinitionId')
    instructions = BodyParameter('instructions')

    def __init__(
        self,
        url: str,
        source_process_definition_id: str,
        target_process_definition_id: str
    ):
        """Validates a migration plan without executing it.

        :param url: Camunda Rest engine URL.
        :param source_process_definition_id: Id of the source process definition for the migration.
        :param target_process_definition_id: Id of the target process definition for the migration.
        """
        super().__init__(url=url + URL_SUFFIX + '/validate')
        self.source_process_definition_id = source_process_definition_id
        self.target_process_definition_id = target_process_definition_id
        self.instructions = []

    def body_parameters(self, apply: typing.Callable = ...) -> typing.Dict[str, typing.Any]:
        params = super().body_parameters(apply=apply)
        params['instructions'] = [
            {
                'sourceActivityIds': instruction.source_activity_ids,
                'targetActivityIds': instruction.target_activity_ids,
                'updateEventTrigger': instruction.update_event_trigger
            }
            for instruction in self.instructions
        ]
        return params

    def add_instruction(
        self,
        source_activity_ids: typing.Iterable[str],
        target_activity_ids: typing.Iterable[str],
        update_event_trigger: bool = False
    ):
        """Add an instruction to validate.

        :param source_activity_ids: The mapped activity ids from the source process definition.
        :param target_activity_ids: The mapped activity ids from the target process definition.
        :param update_event_trigger: Whether event triggers will be updated during migration.
        """
        self.instructions.append(
            MigrationInstruction.load({
                'sourceActivityIds': source_activity_ids,
                'targetActivityIds': target_activity_ids,
                'updateEventTrigger': update_event_trigger}
            )
        )

    @classmethod
    def from_migration_plan(cls, url: str, migration_plan: MigrationPlan) -> Validate:
        """Create an instance of Validate using a MigrationPlan instance.

        :param url: Camunda REST engine url.
        :param migration_plan: The migration plan to create the Validate instance from.
        :return: Validate instance.
        """
        validate_migration = cls(
            url=url,
            source_process_definition_id=migration_plan.source_process_definition_id,
            target_process_definition_id=migration_plan.target_process_definition_id
        )
        validate_migration.instructions = migration_plan.instructions

        return validate_migration

    def __call__(self, *args, **kwargs) -> typing.Tuple[InstructionReport]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)

        return tuple(
            InstructionReport.load(data=report_json)
            for report_json in response.json()['instructionReports']
        )


class Execute(pycamunda.base.CamundaRequest):

    migration_plan = BodyParameter('migrationPlan')
    process_instance_ids = BodyParameter('processInstanceIds')
    process_instance_query = BodyParameter('processInstanceQuery')  # TODO add support for this
    skip_custom_listeners = BodyParameter('skipCustomListeners')
    skip_io_mappings = BodyParameter('skipIoMappings')

    def __init__(
        self,
        url: str,
        source_process_definition_id: str,
        target_process_definition_id: str,
        process_instance_ids: typing.Iterable[str],
        skip_custom_listeners: bool = False,
        skip_io_mappings: bool = False,
        async_: bool = False
    ):
        """Executes a migration plan.

        :param url: Camunda Rest engine URL.
        :param source_process_definition_id: Id of the source process definition for the migration.
        :param target_process_definition_id: Id of the target process definition for the migration.
        :param process_instance_ids: Process instance ids to migrate.
        :param skip_custom_listeners: Whether execution listeners should be invoked.
        :param skip_io_mappings: Whether input / output mappings should be executed.
        :param async_: Whether to run this request asynchronously.
        """
        super().__init__(url=url + URL_SUFFIX + '/execute')
        self.migration_plan = MigrationPlan(
            source_process_definition_id=source_process_definition_id,
            target_process_definition_id=target_process_definition_id,
            instructions=tuple()
        )
        self.process_instance_ids = process_instance_ids
        self.skip_custom_listeners = skip_custom_listeners
        self.skip_io_mappings = skip_io_mappings
        self.async_ = async_

    @property
    def url(self) -> str:
        return super().url + ('Async' if self.async_ else '')

    def body_parameters(self, apply: typing.Callable = ...) -> typing.Dict[str, typing.Any]:
        params = super().body_parameters(apply=apply)
        params['migrationPlan'] = {
            'sourceProcessDefinitionId': self.migration_plan.source_process_definition_id,
            'targetProcessDefinitionId': self.migration_plan.target_process_definition_id,
            'instructions': [
                {
                    'sourceActivityIds': instruction.source_activity_ids,
                    'targetActivityIds': instruction.target_activity_ids,
                    'updateEventTrigger': instruction.update_event_trigger
                } for instruction in self.migration_plan.instructions
            ]
        }
        return params

    def add_instruction(
        self,
        source_activity_ids: typing.Iterable[str],
        target_activity_ids: typing.Iterable[str],
        update_event_trigger: bool = False
    ):
        """Add an instruction to execute.

        :param source_activity_ids: The mapped activity ids from the source process definition.
        :param target_activity_ids: The mapped activity ids from the target process definition.
        :param update_event_trigger: Whether event triggers will be updated during migration.
        """
        self.migration_plan.instructions = tuple(
            [instruction for instruction in self.migration_plan.instructions] + [
                MigrationInstruction.load({
                    'sourceActivityIds': source_activity_ids,
                    'targetActivityIds': target_activity_ids,
                    'updateEventTrigger': update_event_trigger}
                )
            ]
        )

    @classmethod
    def from_migration_plan(
        cls,
        url: str,
        migration_plan: MigrationPlan,
        process_instance_ids: typing.Iterable[str],
        skip_custom_listeners: bool = False,
        skip_io_mappings: bool = False,
        async_: bool = False
    ) -> Execute:
        """Create an instance of Execute using a MigrationPlan instance.

        :param url: Camunda REST engine url.
        :param migration_plan: The migration plan to create the Validate instance from.
        :param process_instance_ids: Process instance ids to migrate.
        :param skip_custom_listeners: Whether execution listeners should be invoked.
        :param skip_io_mappings: Whether input / output mappings should be executed.
        :param async_: Whether to run this request asynchronously.
        :return: Execute instance.
        """
        execute_migration = cls(
            url=url,
            source_process_definition_id=migration_plan.source_process_definition_id,
            target_process_definition_id=migration_plan.target_process_definition_id,
            process_instance_ids=process_instance_ids,
            skip_custom_listeners=skip_custom_listeners,
            skip_io_mappings=skip_io_mappings,
            async_=async_
        )
        for instruction in migration_plan.instructions:
            execute_migration.add_instruction(
                source_activity_ids=instruction.source_activity_ids,
                target_activity_ids=instruction.target_activity_ids,
                update_event_trigger=instruction.update_event_trigger
            )

        return execute_migration

    def __call__(self, *args, **kwargs) -> typing.Optional[pycamunda.batch.Batch]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)

        if self.async_:
            return pycamunda.batch.Batch.load(response.json())
