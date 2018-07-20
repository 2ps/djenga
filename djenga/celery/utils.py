# encoding: utf-8
from functools import wraps
import logging


__all__ = [
    'update_progress',
    'auto_step',
    'unbound_step',
    'substep',
]
logger = logging.getLogger(__name__)


def update_progress(task, progress, *args, **kwargs):
    """
    Adds progress and additional metadata to a celery task.  Since
    celery tasks can also be called as regular ol’ methods, we have
    to handle cases when task.request.id is None (i.e., task.request.id
    is None when a task is called as a regular function instead of with
    `delay` or `apply_async`)
    :param task: celery.Task
    :param progress: format string
    :param args: args for the progress format string
    :param kwargs: additional metadata field/values to set on the task
    """
    if args:
        progress %= args
    request_id = task.request.id
    current = getattr(task.request, 'progress', [])
    current.append(progress)
    if request_id:
        task.backend.mark_as_started(
            request_id,
            progress='\n'.join(current),
            **kwargs)
    setattr(task.request, 'progress', current)
    values = getattr(task.request, 'info', {})
    for key, value in kwargs.items():
        values[key] = value
    setattr(task.request, 'info', values)
    logger.info(progress)


def auto_step(key, description=None,
              start_detail='in progress', end_detail='done'):
    """
    Make sure to apply the `@auto_step` decorator **before** the `@app.task`
    decorator.  e.g.

            @app.task(bind=True, name='my.cool_task',
                      base='djenga.celery.tasks.DetailTask')
            @auto_step(key=1, description='eat cookies')
            def eat_cookies(self):
                pass
    :param key:
    :param description:
    :param start_detail:
    :param end_detail:
    :return:
    """
    def decorator(fn):
        @wraps(fn)
        def decorated(self, *args, **kwargs):
            error = None
            self.start_step(key, description, start_detail)
            try:
                result = fn(self, *args, **kwargs)
                return result
            except Exception as ex:
                error = '%s' % (ex,)
                raise
            finally:
                self.end_step(error, end_detail)
        return decorated
    return decorator


def unbound_step(
        fn, task, key,
        description=None,
        start_detail='in progress',
        end_detail='done'):
    description = description or fn.__name__

    def decorated(*args, **kwargs):
        error = None
        task.start_step(key, description, start_detail)
        try:
            result = fn(*args, **kwargs)
            return result
        except Exception as ex:
            error = '%s' % (ex,)
            raise
        finally:
            task.end_step(error, end_detail)

    return decorated


def substep(task, fn):
    if task:
        task.update_step(fn.__name__)
    return fn
