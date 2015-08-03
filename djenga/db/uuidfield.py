
# encoding: utf-8

from __future__ import unicode_literals
from uuid import UUID
from django.db.backends.mysql.base import django_conversions
from django.db import models


def prep_uuid(
        o,
        *args # pylint: disable=unused-argument
):
    return '0x%s' % o.hex


django_conversions.update({
    UUID: prep_uuid
})


class UuidField(models.fields.Field):
    """
    A Uuid field for MySQL (and MySQL only!) that converts to
    a `binary(16)` on the DB backend.  Unlike many of the implementations
    of binary fields out there (I'm looking at you django 1.6), this
    field does allow the user to do a lookup based on the UUID.

    The related value type of a Uuid field is the `uuid.UUID` class
    from python.
    """
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if isinstance(value, UUID):
            return value
        if value is None:
            return None
        return UUID(bytes=value)

    def get_prep_value(self, value):
        if value is None:
            return 'null'
        if isinstance(value, UUID):
            return value
        try:
            p = UUID(value)
            return p
        except ValueError:
            raise TypeError(
                'A %s cannot be used in a query involving a UUID' % (
                    value.__class__.__name__,
                )
            )

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type not in { 'exact', 'iexact', 'isnull', 'in'}:
            raise TypeError('Binary Fields do not support %s' % lookup_type)
        return self.get_prep_value(value)

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] in { 'django.db.backends.mysql', 'django_mysqlpool.backends.mysqlpool' }:
            return 'binary(16)'
        else:
            raise Exception('MySql is the only defined engine for UuidField.')


