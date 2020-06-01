# -*- coding: utf-8 -*-

import pytest

import pycamunda.filter


def test_filter_load(my_filter_json):
    filter_ = pycamunda.filter.Filter.load(my_filter_json)

    assert filter_.id_ == my_filter_json['id']
    assert filter_.resource_type == my_filter_json['resourceType']
    assert filter_.name == my_filter_json['name']
    assert filter_.owner == my_filter_json['owner']
    assert filter_.query.query_var == my_filter_json['query']['query_var']
    assert filter_.properties.prop_var == my_filter_json['properties']['prop_var']
    assert filter_.item_count == my_filter_json['itemCount']


def test_incident_load_raises_keyerror(my_filter_json):
    for key in (k for k in my_filter_json if k != 'itemCount'):
        json_ = dict(my_filter_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.filter.Filter.load(json_)
    json_ = dict(my_filter_json)
    del json_['itemCount']
    pycamunda.filter.Filter.load(json_)