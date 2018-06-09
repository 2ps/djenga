from __future__ import absolute_import
import os
import importlib
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        if settings.DEBUG:
            from celery import platforms
            # print('root: %s' % (C_FORCE_ROOT,))
            from celery.bin import worker
            module = importlib.import_module(settings.DJENGA_CELERY_MODULE)
            app = module.app
            platforms.C_FORCE_ROOT = True
            w = worker.worker(app)
            queues = { 'celery' }
            routes = getattr(settings, 'CELERY_TASK_ROUTES', None)
            routes = routes or {}
            if isinstance(routes, dict):
                for x in routes.values():
                    queues.add(x['queue'])
            else:
                if isinstance(routes, list) or isinstance(routes, tuple):
                    for route_set in routes:
                        for key, x in route_set:
                            queues.add(x['queue'])
            queues = list(queues)
            w.run(loglevel='info', concurrency=1, queues=queues)
        else:
            return "Sorry, I shouldn't be run in production mode (DEBUG=False)"
