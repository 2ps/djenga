from base64 import b64encode
from base64 import b64decode
import six
from threading import local
import boto3


__all__ = [
    '_as_bytes',
    'b64_str',
    'from_b64_str',
    '_get_client',
    '_prefix_alias',
]


thread_local = local()
thread_local.sessions = {}


def _as_bytes(value):
    if isinstance(value, six.string_types):
        value = value.encode('utf-8')
    return value


def b64_str(value: bytes):
    return b64encode(value).decode('utf-8')


def from_b64_str(value: str):
    value = value.encode('utf-8')
    return b64decode(value)


def _get_client(region: str=None, profile: str=None):
    key = f'{region}-{profile}'
    client = thread_local.sessions.get(key)
    if not client:
        session = boto3.Session(region_name=region, profile_name=profile)
        client = session.client('kms')
        thread_local.sessions[key] = client
    return client


def _prefix_alias(alias: str):
    if not alias.startswith('alias/'):
        alias = f'alias/{alias}'
    return alias


