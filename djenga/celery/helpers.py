
__all__ = [
    u'get_celery_queue_len',
]


def get_celery_queue_len(celery_app, queue_name):
    with celery_app.pool.acquire(block=True) as conn:
        return conn.default_channel.client.llen(queue_name)
