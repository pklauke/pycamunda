# -*- coding: utf-8 -*-

import pytest

import pycamunda.migration


def test_instructionreport_load_definition(my_report_json):

    instruction_report = pycamunda.migration.InstructionReport.load(my_report_json)

    assert instruction_report.instruction == pycamunda.migration.MigrationInstruction.load(
        my_report_json['instruction']
    )
    assert instruction_report.failures == tuple(my_report_json['failures'])


def test_instructionreport_load_raises_key_error(my_report_json):
    for key in my_report_json:
        json_ = dict(my_report_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.migration.InstructionReport.load(data=json_)
