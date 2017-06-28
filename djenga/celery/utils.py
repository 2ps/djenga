# encoding: utf-8
import logging


__all__ = [
    'update_progress',
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
