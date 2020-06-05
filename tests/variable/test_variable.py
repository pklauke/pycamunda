# -*- coding: utf-8 -*-

import pytest

import pycamunda.variable


def test_variable_load():
    variable = pycamunda.variable.Variable.load(
        {'value': 'aVal', 'type': 'String', 'valueInfo': {}, 'local': True}
    )

    assert variable.value == 'aVal'
    assert variable.type_ == 'String'
    assert variable.value_info == {}
    assert variable.local is True


def test_variable_load_raises_keyerror():
    my_variable_json = {'value': 'aVal', 'type': 'String', 'valueInfo': {}, 'local': True}
    for key in (k for k in my_variable_json if k != 'local'):
        json_ = dict(my_variable_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.variable.Variable.load(data=json_)
