from celery.result import AsyncResult


__all__ = [
    'AsyncDetailedResult',
]


class AsyncDetailedResult(AsyncResult):
    def __init__(self, id, backend=None,
                 task_name=None,            # deprecated
                 app=None, parent=None):
        super().__init__(id, backend, task_name, app, parent)

    def details(self):
        meta = self._get_task_meta()
        return meta.get('details') if meta else []
