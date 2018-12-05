from collections import OrderedDict, defaultdict
from functools import partial
import logging
import os
import re
from typing import Any
from typing import List
from typing import Dict
from typing import Union
import yaml
from .bunch import Bunch


__all__ = [
    'ConfigBunch',
    'KmsBunch',
    'LazySecret',
    'LazyKmsBunch',
]
logger = logging.getLogger(__name__)


class ConfigBunch(Bunch):
    def __init__(self, *filenames: str, **kwargs):
        """
        initialize with a list of files to be
        read, in order.  nested dicts
        are not supported, but you can
        use dotted key names to achieve the same effect.
        :type filenames: List[str]
        """
        super().__init__()
        for x in filenames:
            try:
                with open(x, 'r') as f:
                    logger.debug('[djenga]  loading settings from [%s]', x)
                    values = self.load_file(f)
                    self.assimilate_values(values)
            except FileNotFoundError:
                logger.debug('[djenga]  file [%s] was not found, skipping.', x)

    def load_file(self, f):
        values: Dict[str, Any] = yaml.load(f)
        return values

    def assimilate_values(self, values):
        if not isinstance(values, dict):
            logger.warning('[djenga]  invalid format, skipping')
            return
        for key, value in values.items():
            pieces: List[str] = key.split('.')
            parent = self.create_to_parent(pieces)
            setattr(parent, pieces[-1], value)

    def create_to_parent(self, pieces: List[str]) -> 'ConfigBunch':
        parent: ConfigBunch = self
        for y in pieces[:-1]:
            if not hasattr(parent, y):
                child = ConfigBunch()
                setattr(parent, y, child)
            else:
                child = getattr(parent, y)
            parent = child
        return parent

    def walk_to_parent(self, pieces: List[str]) -> 'ConfigBunch':
        parent: ConfigBunch = self
        for x in pieces[:-1]:
            parent = getattr(parent, x, None)
            if not isinstance(parent, Bunch):
                return None
        return parent

    def get(self, key, default=None):
        pieces = key.split('.')
        parent = self.walk_to_parent(pieces)
        if parent:
            return getattr(parent, pieces[-1], default)
        return default

    def __getitem__(self, key):
        pieces = key.split('.')
        parent = self.walk_to_parent(pieces)
        if parent:
            return getattr(parent, pieces[-1])
        raise KeyError(f'{key} not found in config')

    def __setitem__(self, key, value):
        pieces = key.split('.')
        parent = self.create_to_parent(pieces)
        setattr(parent, pieces[-1], value)

    def setdefault(self, key, value):
        pieces = key.split('.')
        parent = self.create_to_parent(pieces)
        key = pieces[-1]
        if hasattr(parent, key):
            return getattr(parent, key)
        setattr(parent, key, value)
        return value

    def env(self):
        splitter = re.compile(r'[_.]')

        def fn(key, default=None):
            value = os.environ.get(key)
            if not value:
                pieces = splitter.split(key.lower())
                parent: ConfigBunch = self.walk_to_parent(pieces)
                if not isinstance(parent, ConfigBunch):
                    return None
                value = parent.get(pieces[-1], default)
            return value
        return fn


class KmsBunch(ConfigBunch):
    def __init__(self, *filenames: str, **kwargs):
        """
        initialize with a list of files to be
        read, in order.  nested dicts
        are not supported, but you can
        use dotted key names to achieve the same effect.
        :type filenames: List[str]
        :type kms_key_id: str
        :type profile: str
        :type region: str
        """
        super().__init__()
        self.profile: str = kwargs.get('profile', None)
        self.region: str = kwargs.get('region', None)
        for x in filenames:
            try:
                with open(x, 'r') as f:
                    logger.debug('[djenga]  loading settings from [%s]', x)
                    values = self.load_file(f)
                    values = self.decrypt(values)
                    self.assimilate_values(values)
            except FileNotFoundError:
                logger.debug('[djenga]  file [%s] was not found, skipping.', x)

    def decrypt(self, values):
        from djenga.encryption.kms_wrapped import decrypt
        if isinstance(values, list) or isinstance(values, tuple):
            return [ self.decrypt(x) for x in values ]
        if isinstance(values, dict) or isinstance(values, OrderedDict) or isinstance(values, defaultdict):
            return {
                key: self.decrypt(value)
                for key, value in values.items()
            }
        try:
            return decrypt(values, region=self.region, profile=self.profile)
        except:
            return values


class LazySecret:
    def __init__(self, value=None, decrypt_fn=None):
        self.decrypted = False
        self.value = value
        self.decrypt = decrypt_fn

    def get(self):
        return self.decrypt(self.value)


class LazyKmsBunch(ConfigBunch):
    def __init__(self, *filenames: str, **kwargs):
        """
        initialize with a list of files to be
        read, in order.  nested dicts
        are not supported, but you can
        use dotted key names to achieve the same effect.
        :type filenames: List[str]
        :type kms_key_id: str
        :type profile: str
        :type region: str
        """
        from djenga.encryption.kms_wrapped import decrypt
        super().__init__()
        self.profile: str = kwargs.get('profile', None)
        self.region: str = kwargs.get('region', None)
        self.decrypt_fn = partial(decrypt, region=self.region, profile=self.profile)
        for x in filenames:
            try:
                with open(x, 'r') as f:
                    logger.debug('[djenga]  loading settings from [%s]', x)
                    values = self.load_file(f)
                    values = self.lazy_wrap(values)
                    self.assimilate_values(values)
            except FileNotFoundError:
                logger.debug('[djenga]  file [%s] was not found, skipping.', x)

    def lazy_wrap(self, values: Union[Dict, List, str]):
        if isinstance(values, list) or isinstance(values, tuple):
            return [ self.lazy_wrap(x) for x in values ]
        if isinstance(values, dict) or isinstance(values, OrderedDict) or isinstance(values, defaultdict):
            return {
                key: self.lazy_wrap(value)
                for key, value in values.items()
            }
        if isinstance(values, str) and values.count('|') == 4:
            return LazySecret(values, self.decrypt_fn)
        return values
