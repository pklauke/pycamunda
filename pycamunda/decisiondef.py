# -*- coding: utf-8 -*-

"""This module provides access to the decision definition REST api of Camunda."""

from __future__ import annotations
import typing
import dataclasses


@dataclasses.dataclass
class DecisionDefinition:
    """Data class of decision definition as returned by the REST api of Camunda."""
    id_: str
    key: str
    category: str
    name: str
    version: int
    resource: str
    deployment_id: str
    decision_requirements_definition_id: str
    decision_requirements_definition_key: str
    tenant_id: str
    version_tag: str
    history_time_to_live: int

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> DecisionDefinition:
        return cls(
            id_=data['id'],
            key=data['key'],
            category=data['category'],
            name=data['name'],
            version=data['version'],
            resource=data['resource'],
            deployment_id=data['deploymentId'],
            decision_requirements_definition_id=data['decisionRequirementsDefinitionId'],
            decision_requirements_definition_key=data['decisionRequirementsDefinitionKey'],
            tenant_id=data['tenantId'],
            version_tag=data['versionTag'],
            history_time_to_live=data['historyTimeToLive']
        )
