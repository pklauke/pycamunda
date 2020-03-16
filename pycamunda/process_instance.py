# -*- coding: utf-8 -*-

from __future__ import annotations
import dataclasses
import typing

import pycamunda.variable


@dataclasses.dataclass
class ProcessInstance:
    id_: str
    definition_id: str
    business_key: str
    case_instance_id: str
    tenant_id: str
    ended: bool
    suspended: bool
    links: typing.Tuple[pycamunda.Link]
    variables: typing.Dict[str, pycamunda.variable.Variable] = None

    @classmethod
    def load(cls, data) -> ProcessInstance:
        process_instance = cls(
            id_=data['id'],
            definition_id=data['definitionId'],
            business_key=data['businessKey'],
            case_instance_id=data['caseInstanceId'],
            tenant_id=data['tenantId'],
            ended=data['ended'],
            suspended=data['suspended'],
            links=tuple(pycamunda.Link.load(link_json) for link_json in data['links']),
        )
        try:
            variables = data['variables']
        except KeyError:
            pass
        else:
            process_instance.variables = {name: pycamunda.variable.Variable.load(var_json)
                                          for name, var_json in variables.items()}

        return process_instance
