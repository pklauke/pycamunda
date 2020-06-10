# -*- coding: utf-8 -*-

"""This module provides instruction enumerations as returned by the REST api of Camunda."""

import enum


class InstructionType(enum.Enum):
    start_before_activity = 'startBeforeActivity'
    start_after_activity = 'startAfterActivity'
    start_transition = 'startTransition'


class ModifyInstructionType(enum.Enum):
    start_before_activity = 'startBeforeActivity'
    start_after_activity = 'startAfterActivity'
    start_transition = 'startTransition'
    cancel = 'cancel'
