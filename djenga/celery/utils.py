import logging


__all__ = [
    'add_progress',
]
logger = logging.getLogger(__name__)


def add_progress(task, progress, *args, **kwargs):
    """
    Adds progress and additional metadata to a celery task
    :param task: celery.Task
    :param progress: format string
    :param args: args
    :param kwargs: additional metadata field/values to set on the task
    """
    request_id = task.request.id
    current = getattr(task.request, 'progress', [])
    if args:
        current.append(progress % args)
        logger.info(progress, *args)
    else:
        current.append(progress)
        logger.info(progress)
    task.backend.mark_as_started(
        request_id,
        progress='\n'.join(current),
        **kwargs)
    setattr(task.request, 'progress', current)
