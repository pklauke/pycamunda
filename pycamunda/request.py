# -*- coding: utf-8 -*-

import abc
from typing import Mapping, Callable

import pycamunda


def value_is_true(self, obj, obj_type):
    return obj.__dict__[self.key]


class RequestParameter:

    def __init__(self, key, mapping: Mapping=None, provide: Callable=None, validate: Callable=None):
        """Parameter that is send with a CamundaRequest when it is attached to the class and its
        value is set. This class implements the descriptor protocol.

        :param key: Camunda key of the request parameter.
        :param mapping: Mapping from descriptor value to the parameter that is send to Camunda.
        :param provide: Callable that determines whether the value is returned. Is expected to
                        accept 3 arguments:
                            - Descriptor instance,
                            - Object instance the descriptor is attached to and
                            - Type of the object the descriptor is attached to.
        :param validate: Callable that validates the value that is tried to be set.
        """
        self.key = key
        self.mapping = mapping
        self.provide = provide
        self.validate = validate
        self.name = None

    def __get__(self, obj, obj_type=None):
        if self.provide is None or self.provide(self, obj, obj_type):
            if self.mapping is None:
                return obj.__dict__[self.name]
            return self.mapping[obj.__dict__[self.name]]

    def __set__(self, obj, value):
        if self.validate is not None and not self.validate(value):
            raise pycamunda.PyCamundaInvalidInput(f'Cannot set value "{value}" for "{self.name}"')
        obj.__dict__[self.name] = value

    def __repr__(self):
        return f'{self.__class__.__qualname__}(key=\'{self.key}\')'


class QueryParameter(RequestParameter):
    """Parameter that is attached to the request URL by adding it after the endpoint name."""


class PathParameter(RequestParameter):

    def __init__(self, *args, **kwargs):
        """Parameter that is attached to the request URL by adding it to the endpoint name."""
        super().__init__(*args, **kwargs)
        self.instance = None

    def __call__(self, *args, **kwargs):
        return getattr(self.instance, self.name)


class BodyParameter(RequestParameter):

    def __init__(self, *args, **kwargs):
        """Parameter that is attached to the request body."""
        super().__init__(*args, **kwargs)
        self.hidden = False


class BodyParameterContainer:
    """Stores multiple BodyParameters`s and allows sending nested queries.

    :param key: Camunda key.
    :param args: BodyParameter`s
    """
    def __init__(self, key, *parameters):
        self.key = key
        self.parameters = {}
        for parameter in parameters:
            self.parameters[parameter.key] = parameter
            parameter.hidden = True

    def __repr__(self):
        return f'{self.__class__.__qualname__}(key={self.key}, ' \
               f'{", ".join(k+"="+str(v) for k, v in self.parameters.items())})'


class CamundaRequestMeta(abc.ABCMeta):

    def __init__(cls, name, bases, attr_dict):

        super().__init__(name, bases, attr_dict)

        try:
            cls._parameters = dict(cls._parameters)
        except AttributeError:
            cls._parameters = {}
        try:
            cls._containers = dict(cls._containers)
        except AttributeError:
            cls._containers = {}

        for key, attr in attr_dict.items():
            if isinstance(attr, RequestParameter):
                attr.name = key
                cls._parameters[key] = attr
            elif isinstance(attr, BodyParameterContainer):
                cls._containers[key] = attr


class CamundaRequest(metaclass=CamundaRequestMeta):

    def __init__(self, url):
        """Abstract base class for Camunda requests. Extracts parameters to send with the requests
        by parsing the class for RequestParameter`s.

        :param url: Camunda Rest engine url.
        """
        super().__init__()
        self._url = url

        for name, attribute in self._parameters.items():
            if isinstance(attribute, PathParameter):
                attribute.instance = self  # TODO Fix incorrect instance assignment when Pathparameter is overwritten in child class

    @property
    def url(self):
        params = {}
        missing_params = {}
        for name, attribute in self._parameters.items():
            print(name, attribute, isinstance(attribute, PathParameter))
            if isinstance(attribute, PathParameter):
                try:
                    params[attribute.key] = attribute()
                except AttributeError:
                    missing_params[attribute.key] = ''
        return self._url.format(**{**params, **missing_params}).rstrip('/')

    def __call__(self, *args, **kwargs):
        return self.send(*args, **kwargs)

    @abc.abstractmethod
    def send(self):
        return NotImplementedError

    def query_parameters(self):
        query = {}
        for name, attribute in self._parameters:
            if isinstance(attribute, QueryParameter):
                try:
                    query[attribute.key] = getattr(self, attribute.name)
                except KeyError:
                    pass
        return query

    def _traverse(self, container):
        query = {}
        for key, val in container.parameters.items():
            if isinstance(val, BodyParameterContainer):
                query[key] = self._traverse(val)
            else:
                try:
                    value = getattr(self, val.name)
                except KeyError:
                    pass
                except AttributeError:
                    if val is not None:
                        query[key] = val
                else:
                    if value is not None:
                        query[key] = value
        return query

    def body_parameters(self):
        query = {}
        for name, attribute in self._containers.items():
            if isinstance(attribute, BodyParameterContainer):
                query[attribute.key] = self._traverse(attribute)
        for name, attribute in self._parameters.items():
            if isinstance(attribute, BodyParameter) and not attribute.hidden:
                try:
                    value = getattr(self, attribute.name)
                except KeyError:
                    pass
                else:
                    if value is not None:
                        query[attribute.key] = value

        return query
