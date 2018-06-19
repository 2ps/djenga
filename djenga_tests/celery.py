from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.signals import after_setup_logger
from celery.signals import worker_process_init
from djenga.celery.tasks import DetailTask


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djenga_tests.settings')


class DjengaCelery(Celery):
    def __init__(self, main=None, loader=None, backend=None,
                 amqp=None, events=None, log=None, control=None,
                 set_as_current=True, tasks=None, broker=None, include=None,
                 changes=None, config_source=None, fixups=None, task_cls=None,
                 autofinalize=True, namespace=None, strict_typing=True,
                 **kwargs):
        from djenga.celery.tasks import DetailTask
        from djenga.celery.backends import patch_aliases
        patch_aliases()
        super().__init__(main, loader, backend, amqp, events, log, control,
                         set_as_current, tasks, broker, include, changes,
                         config_source, fixups, task_cls=DetailTask,
                         autofinalize=autofinalize, namespace=namespace,
                         strict_typing=strict_typing, **kwargs)

    def now(self):
        """Return the current time and date as a datetime."""
        from datetime import datetime
        return datetime.now(self.timezone)


app = DjengaCelery('djenga_tests')


# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.broker_transport_options = {'visibility_timeout': 86400}
n = 0


@app.task(bind=True, steps=[
    ( 1, 'get logger',),
    ( 2, 'increment n',),
    ( 3, 'output debugging',), ]
)
def debug_task(self):
    """:type self: djenga.celery.tasks.DetailTask"""
    import logging
    import time
    self.start_step(1)
    logger = logging.getLogger(__name__)
    time.sleep(30)
    self.end_step()
    self.start_step(2)
    global n
    n += 1
    time.sleep(45)
    self.end_step()
    self.start_step(3)
    logger.info('request type: %s', type(self.request))
    print('{0} Request: {1!r}'.format(n, self.request))
    time.sleep(60)
    self.end_step()
    logger.info('details: ')
    for x in self.request.details.values():
        logger.info('  - %s [%s]', x, x.done)


@app.task(bind=True, base=DetailTask)
def error_task(self):
    import logging
    logger = logging.getLogger(__name__)
    global n
    n += 1
    logger.info('request type: %s', type(self.request))
    logger.error('{0} Request: {1!r}'.format(n, self.request))


def update_loglevel(*args, **kwargs):
    app.log.redirect_stdouts(loglevel='INFO')


# it's not at all clear to me why these
# two signals work, or the correct timing at
# which to call the function to redirect the
# stdouts, but this worked, so I felt it
# was wise to just go with it . . .
after_setup_logger.connect(update_loglevel)
worker_process_init.connect(update_loglevel)

from djenga.celery.utils import auto_step


@auto_step(key=1)
def fly_to_the_moon(self):
    pass


@auto_step(key=2)
def shrink_the_moon(self):
    pass


@auto_step(key=3)
def grab_the_moon(self):
    pass


@auto_step(key=4)
def sit_on_the_toilet(self):
    pass


@app.task(bind=True, base=DetailTask, steps=[
            (1, 'Fly to the moon'), (2, 'Shrink the moon'),
            (3, 'Grab the moon'), (4, 'Sit on the toilet'),])
def steal_the_moon(self):
    fly_to_the_moon(self)
    shrink_the_moon(self)
    grab_the_moon(self)
    sit_on_the_toilet(self)
