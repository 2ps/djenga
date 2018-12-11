"""
MySQL database backend for Django.

Requires mysqlclient: https://pypi.org/project/mysqlclient/
"""
from django.db.backends.mysql.base import CLIENT, FIELD_TYPE                # isort:skip
from django.db.backends.mysql.base import conversions                      # isort:skip

# Some of these import MySQLdb, so import them after checking if it's installed.
from .client import DatabaseClient                          # isort:skip
from django.db.backends.mysql.creation import DatabaseCreation                      # isort:skip
from django.db.backends.mysql.features import DatabaseFeatures                      # isort:skip
from django.db.backends.mysql.introspection import DatabaseIntrospection            # isort:skip
from django.db.backends.mysql.operations import DatabaseOperations                  # isort:skip
from django.db.backends.mysql.schema import DatabaseSchemaEditor                    # isort:skip
from django.db.backends.mysql.validation import DatabaseValidation                  # isort:skip
from django.db.backends.mysql.base import DatabaseWrapper as ParentDatabaseWrapper
from django.db.backends.mysql.base import version
from django.db.backends.mysql.base import CursorWrapper


class DatabaseWrapper(ParentDatabaseWrapper):
    client_class = DatabaseClient
    def get_connection_params(self):
        from djenga.core import LazySecret
        kwargs = super().get_connection_params()
        password = kwargs.get('passwd')
        if isinstance(password, LazySecret):
            kwargs['passwd'] = password.get()
        return kwargs
