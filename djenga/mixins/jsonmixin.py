# encoding: utf-8
# pylint: disable=pointless-string-statement


from datetime import datetime
from datetime import date
from decimal import Decimal
from django.db import models


class JsonMixin(object):
    def to_json(self):
        mp = {}
        rg_fields = self._meta.get_all_field_names()
        for x in rg_fields:
            try:
                p_field = self._meta.get_field(x)
                if isinstance(p_field, models.ForeignKey):
                    continue
                value = getattr(self, x, None)
                if isinstance(value, Decimal):
                    mp[x] = float(value)
                elif isinstance(value, date) or isinstance(value, datetime):
                    mp[x] = '%s' % value
                else:
                    mp[x] = value
            except models.FieldDoesNotExist:
                mp[x] = getattr(self, x, None)
        return mp