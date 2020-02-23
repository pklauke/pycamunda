# -*- coding: utf-8 -*-


class PyCamundaException(Exception):
    """Base class for all PyCamunda exceptions."""


class PyCamundaNoSuccess(PyCamundaException):
    """Exception that is raised when a response is not successful."""


class PyCamundaUserAlreadyExists(PyCamundaNoSuccess):
    """Exception that is raised when it is tried to create a user that already exists."""
