from __future__ import absolute_import
from collections import OrderedDict
import logging
from time import time
from celery.app.task import Task, Context
from celery import states


__all__ = [
    'DetailTask',
    'TaskDetail',
]
logger = logging.getLogger(__name__)


class TaskDetail:
    def __init__(self, key=None, description=None, *args, **kwargs):
        """
        :type key: str
        :type description: str
        """
        self.key = key
        self.description = description
        self.detail = []
        self.millis = None
        self.done = False
        self.error = False

    def add_detail(self, detail):
        self.detail.append(detail)

    def start_time(self):
        self.millis = time()

    def end_time(self):
        self.done = True
        self.millis = int(1000 * (time() - (self.millis or 0)))

    def to_json(self):
        return {
            'key': self.key,
            'description': self.description,
            'details': self.detail,
            'latest': self.detail[-1] if self.detail else None,
            'time': self.millis,
            'error': self.error,
            'done': self.done,
        }

    def __str__(self):
        return '%s: %s' % (self.key, self.description,)


class DetailTask(Task):
    steps = None

    def __init__(self, steps=None):
        super().__init__()
        self.steps = self.steps or []
        self.details = OrderedDict()
        for key, description in self.steps:
            self.details[key] = description

    def initialize_detail(self):
        if not hasattr(self.request, 'details'):
            self.request.details = OrderedDict([
                (key, TaskDetail(key, description),)
                for key, description in self.details.items()
            ])
            """:type dict[str, TaskDetail]"""
            self.request.detail_stack = list()
            self.request.current_detail = None

    def save_details(self):
        if self.request.id:
            self.backend.store_result(
                self.request.id,
                result=None,
                state=states.STARTED,
                details=self.request.details)

    def start_step(self, key, description=None, detail='in progress'):
        self.initialize_detail()
        r = self.request
        if key not in r.details:
            r.current_detail = r.details.setdefault(
                key, TaskDetail(key, description))
        else:
            r.current_detail = r.details[key]
        r.current_detail.start_time()
        r.current_detail.add_detail(detail)
        r.detail_stack.append(r.current_detail)
        logger.info(
            '[%s/%s] %s', r.current_detail.key,
            r.current_detail.description, detail)
        self.save_details()

    def update_step(self, detail, *args):
        self.initialize_detail()
        r = self.request
        if args:
            try:
                detail = detail % args
            except Exception as ex:
                logger.exception('%s', ex)
        r.current_detail.add_detail(detail)
        logger.info(
            '[%s/%s] %s', r.current_detail.key,
            r.current_detail.description, detail)
        self.save_details()

    def end_step(self, error=None, detail='done'):
        self.initialize_detail()
        r = self.request
        if error:
            r.current_detail.error = error
            r.current_detail.add_detail(error)
            logger.info(
                '[%s/%s] %s', r.current_detail.key,
                r.current_detail.description, error)
        else:
            r.current_detail.add_detail(detail)
            logger.info(
                '[%s/%s] %s', r.current_detail.key,
                r.current_detail.description, detail)
        r.current_detail.end_time()
        r.detail_stack.pop()
        if r.detail_stack:
            r.current_detail = r.detail_stack[-1]
        else:
            r.current_detail = None
        self.save_details()
