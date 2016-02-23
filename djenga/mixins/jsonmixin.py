# encoding: utf-8
# pylint: disable=pointless-string-statement


from datetime import datetime
from datetime import date
from decimal import Decimal
from django.db import models


class JsonMixin(object):
    def to_json(self):
        def get_json_value(data, field, field_name=None):
            if isinstance(field, models.ForeignKey):
                field_name = field.name + '_id' or field_name
            else:
                field_name = field_name or field.name
            value = getattr(self, field_name, None)
            if isinstance(value, Decimal):
                data[field_name] = float(value)
            elif isinstance(value, date) or isinstance(value, datetime):
                data[field_name] = value.isoformat()
            else:
                data[field_name] = value

        mp = {}
        p = self._meta
        fn = getattr(p, 'get_fields', None)
        if fn:
            for x in fn():
                get_json_value(mp, x)
        else:
            rg_fields = p.get_all_field_names()
            for x in rg_fields:
                try:
                    p_field = p.get_field(x)
                    get_json_value(mp, p_field, x)
                except models.FieldDoesNotExist:
                    mp[x] = getattr(self, x, None)
        return mp
