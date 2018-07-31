import logging
import os
from typing import Any
from typing import List
from typing import Dict
import yaml
from .bunch import Bunch


__all__ = [
    'ConfigBunch',
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
                    values: Dict[str, Any] = yaml.load(f)
                    if not isinstance(values, dict):
                        logger.warning('[djenga]  invalid format, skipping')
                        continue
                    for key, value in values.items():
                        pieces: List[str]  = key.split('.')
                        parent = self.create_to_parent(pieces)
                        setattr(parent, pieces[-1], value)
            except FileNotFoundError:
                logger.debug('[djenga]  file [%s] was not found, skipping.', x)

    def create_to_parent(self, pieces: List[str]) -> 'ConfigBunch':
        parent: ConfigBunch = self
        for y in pieces[:-1]:
            if not hasattr(parent, y):
                setattr(parent, y, ConfigBunch())
            parent = getattr(parent, y)
        return parent

    def walk_to_parent(self, pieces: List[str]) -> 'ConfigBunch':
        parent: ConfigBunch = self
        for x in pieces[:-1]:
            parent = getattr(parent, x, None)
            if not isinstance(parent, Bunch):
                return None
        return parent

    def get(self, key, default=None):
        pieces = key.split(':')
        parent = self.walk_to_parent(pieces)
        return getattr(parent, key, default)

    def __getitem__(self, key):
        pieces = key.split(':')
        parent = self.walk_to_parent(pieces)
        return getattr(parent, key)

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
        def fn(key, default=None):
            value = os.environ.get(key)
            if not value:
                pieces = key.lower().split('_')
                parent: ConfigBunch = self.walk_to_parent(pieces)
                if not isinstance(parent, ConfigBunch):
                    return None
                value = parent.get(pieces[-1], default)
            return value
        return fn
