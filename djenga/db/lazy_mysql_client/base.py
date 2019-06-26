"""
MySQL database backend for Django.

Requires mysqlclient: https://pypi.org/project/mysqlclient/
"""
from django.db.backends.mysql.base import DatabaseWrapper as _DatabaseWrapper
from .client import DatabaseClient


class DatabaseWrapper(_DatabaseWrapper):
    client_class = DatabaseClient

    def get_connection_params(self):
        from ...core import LazySecret
        kwargs = super().get_connection_params()
        password = kwargs.get('passwd')
        if isinstance(password, LazySecret):
            kwargs['passwd'] = password.get()
        return kwargs
