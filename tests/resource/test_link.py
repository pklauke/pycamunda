# -*- coding: utf-8 -*-

import pytest

import pycamunda.resource


def test_link_load(my_link_json):
    link = pycamunda.resource.Link.load(my_link_json)

    assert link.method == my_link_json['method']
    assert link.href == my_link_json['href']
    assert link.rel == my_link_json['rel']


def test_link_load_raises_keyerror(my_link_json):
    for key in my_link_json:
        json_ = dict(my_link_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.resource.Link.load(json_)
