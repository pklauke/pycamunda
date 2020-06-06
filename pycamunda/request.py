# -*- coding: utf-8 -*-

import abc
import typing


class InvalidInput(ValueError):
    """Exception that is raised when invalid input is provided."""


class RequestParameter:

    def __init__(
        self,
        key: str,
        mapping: typing.Mapping = None,
        provide: typing.Callable = None,
        validate: typing.Callable = None
    ):
        """Parameter that is send with a Request when it is attached to the class and its value is
        set. This class implements the descriptor protocol.

        :param key: Api key of the request parameter.
        :param mapping: Mapping from descriptor value to the parameter that is send.
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

    def __get__(self, obj: typing.Any, obj_type: typing.Any = None) -> typing.Any:
        if self.provide is None or self.provide(self, obj, obj_type):
            if self.mapping is None:
                return obj.__dict__[self.name]
            return self.mapping[obj.__dict__[self.name]]

    def __set__(self, obj: typing.Any, value: typing.Any):
        if self.validate is not None and not self.validate(value):
            raise InvalidInput(f'Cannot set value "{value}" for "{self.name}"')
        obj.__dict__[self.name] = value

    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}(key=\'{self.key}\')'


class QueryParameter(RequestParameter):
    """Parameter that is attached to the request URL by adding it after the endpoint name."""


class PathParameter(RequestParameter):
    """Parameter that is attached to the request URL by adding it to the endpoint name."""


class BodyParameter(RequestParameter):

    def __init__(self, *args, **kwargs):
        """Parameter that is attached to the request body."""
        super().__init__(*args, **kwargs)
        self.hidden = False


class BodyParameterContainer:
    """Stores multiple BodyParameters and allows sending nested queries.

    :param key: Key for the nested query.
    :param args: BodyParameter`s
    """
    def __init__(self, key: str, *parameters):
        self.key = key
        self.parameters = {}
        for parameter in parameters:
            self.parameters[parameter.key] = parameter
            parameter.hidden = True

    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}(key={self.key}, ' \
               f'{", ".join(k+"="+str(v) for k, v in self.parameters.items())})'


class RequestMeta(abc.ABCMeta):

    def __init__(cls, name: str, bases: typing.Any, attr_dict: typing.Dict[str, typing.Any]):

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


class Request(metaclass=RequestMeta):

    def __init__(self, url: str):
        """Abstract base class for requests. Extracts parameters to send with the requests by
        parsing the class for RequestParameter`s.

        :param url: Rest engine url.
        """
        super().__init__()
        self._url = url

    @property
    def url(self) -> str:
        params = {}
        missing_params = {}
        for name, attribute in self._parameters.items():
            if isinstance(attribute, PathParameter):
                try:
                    params[attribute.key] = getattr(self, attribute.name)
                except AttributeError:
                    missing_params[attribute.key] = ''
        return self._url.format(**{**params, **missing_params}).rstrip('/')

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        return NotImplementedError

    def query_parameters(self, apply: typing.Callable = None) -> typing.Dict[str, typing.Any]:
        query = {}
        for name, attribute in self._parameters.items():
            if isinstance(attribute, QueryParameter):
                try:
                    value = getattr(self, attribute.name)
                except KeyError:
                    pass
                else:
                    if value is not None:
                        query[attribute.key] = value

        if apply is None:
            return query
        return {key: apply(value) for key, value in query.items()}

    def _traverse(self, container: BodyParameterContainer) -> typing.Dict[str, typing.Any]:
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

    def body_parameters(self, apply: typing.Callable = None) -> typing.Dict[str, typing.Any]:
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

        if apply is None:
            return query
        return {key: apply(value) for key, value in query.items()}
