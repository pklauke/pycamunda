# -*- coding: utf-8 -*-

"""This module provides access to the case instance REST api of Camunda."""


from __future__ import annotations
import dataclasses
import typing


__all__ = []


@dataclasses.dataclass
class CaseInstance:
    """Data class of case instance as returned by the REST api of Camunda."""
    id_: str
    definition_id: str
    tenant_id: str
    business_key: str
    active: bool

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> CaseInstance:
        case_instance = cls(
            id_=data['id'],
            definition_id=data['caseDefinitionId'],
            tenant_id=data['tenantId'],
            business_key=data['businessKey'],
            active=data['active']
        )

        return case_instance
