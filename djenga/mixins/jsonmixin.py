# encoding: utf-8
# pylint: disable=pointless-string-statement

from collections import Iterable
from datetime import datetime
from datetime import date
from decimal import Decimal
import json
from dateutil import parser as date_parser
from django.db import models


__all__ = [
    'JsonMixin',
    'to_json',
    'from_json',
]


def make_json_serializable(value, fn=lambda x: x):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return fn(value)


class JsonEncoder(json.JSONEncoder):
    def default(self, value):
        return make_json_serializable(value, super(JsonEncoder, self).default)


def pairs_hook(pairs):
    data = {}
    for key, value in pairs:
        if not isinstance(value, basestring):
            data[key] = value
        else:
            try:
                data[key] = date_parser.parse(value)
            except ValueError:
                data[key] = value
    return data


def to_json(p, additional_fields=None):
    if not isinstance(p, models.Model):
        raise ValueError('The record provided is not a models.Model instance')
    fn = getattr(p._meta, 'get_fields', None)
    data = {}
    if fn:
        for x in fn():
            field_name = x.name + '_id' if isinstance(x, models.ForeignKey) else x.name
            data[field_name] = make_json_serializable(getattr(p, field_name, None))
    else:
        # Handle pre-django 1.9
        for x in p._meta.get_all_field_names():
            try:
                field = p._meta.get_field(x)
                field_name = x + '_id' if isinstance(field, models.ForeignKey) else x
                data[field_name] = make_json_serializable(getattr(p, field_name, None))
            except models.FieldDoesNotExist:
                data[x] = getattr(p, x, None)
    if additional_fields and isinstance(additional_fields, Iterable):
        for x in additional_fields:
            data[x] = getattr(p, x, None)
    return data


def from_dict(p, data):
    for key, value in data.items():
        setattr(p, key, value)


def from_json(p, data):
    data = json.loads(data, object_pairs_hook=pairs_hook)
    for key, value in data.items():
        setattr(p, key, value)


class JsonMixin(object):
    def to_json(self, additional_fields=None):
        return to_json(self, additional_fields)

    def from_json(self, data):
        pass