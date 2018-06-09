from celery.backends.redis import RedisBackend
from collections import OrderedDict


__all__ = [
    'RedisDetailBackend',
    'patch_aliases',
]


class RedisDetailBackend(RedisBackend):
    def _store_result(self, task_id, result, state,
                      traceback=None, request=None, **kwargs):
        """
        :type task_id: str
        :type result: object
        :type status: dict
        :type traceback: object
        :type request: djenga.celery.tasks.StatusContext
        :param kwargs:
        :return:
        """
        if request:
            details = getattr(request, 'details', None)
        else:
            details = kwargs.get('details')
        if isinstance(details, OrderedDict):
            details = [ x.to_json() for x in details.values() ]
        meta = {
            'status': state,
            'result': result,
            'traceback': traceback,
            'children': self.current_task_children(request),
            'details': details,
        }
        self.set(self.get_key_for_task(task_id), self.encode(meta))
        return result


def patch_aliases():
    from celery.app.backends import BACKEND_ALIASES
    BACKEND_ALIASES['redisd'] = 'djenga.celery.backends.RedisDetailBackend'


