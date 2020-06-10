# -*- coding: utf-8 -*-

"""This module provides access to the execution REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing


@dataclasses.dataclass
class Execution:
    """Data class of execution as returned by the REST api of Camunda."""
    id_: str
    process_instance_id: str
    ended: bool
    tenant_id: str

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> Execution:
        return cls(
            id_=data['id'],
            process_instance_id=data['processInstanceId'],
            ended=data['ended'],
            tenant_id=data['tenantId']
        )
