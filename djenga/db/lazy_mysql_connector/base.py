"""
MySQL database backend for Django.

Requires mysqlclient: https://pypi.org/project/mysqlclient/
"""
from django.db.backends.mysql.base import CLIENT, FIELD_TYPE                # isort:skip
from django.db.backends.mysql.base import conversions                      # isort:skip

# Some of these import MySQLdb, so import them after checking if it's installed.
from .client import DatabaseClient                          # isort:skip
from mysql.connector.django.base import DatabaseWrapper as ParentDatabaseWrapper
from mysql.connector.django.base import version


class DatabaseWrapper(ParentDatabaseWrapper):
    client_class = DatabaseClient

    def get_connection_params(self):
        from djenga.core import LazySecret
        kwargs = super().get_connection_params()
        password = kwargs.get('passwd')
        if isinstance(password, LazySecret):
            kwargs['passwd'] = password.get()
        return kwargs
