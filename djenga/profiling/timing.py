# encoding: utf-8
# pylint: disable=pointless-string-statement

from __future__ import unicode_literals
import threading
from time import time
from django.db import connections


timers = threading.local()


def query_count():
    n_queries = 0
    for x in connections:
        n_queries += len(connections[x].queries)
    return n_queries


def start_timer(logger, name, count_queries=False):
    """
    @type logger: logging.Logger | djenga.mixins.LoggingMixin
    @type name: basestring
    @type count_queries: bool
    """
    if not hasattr(timers, 'stack'):
        timers.stack = list()
        """@type: list[(logging.Logger, basestring, float, bool, int)]"""
    stack = timers.stack
    tm_start = time()
    n_queries = query_count()
    stack.append((logger, name, tm_start, count_queries, n_queries))
    logger.info('%sStarting %s', '-' * len(stack), name)


def end_timer():
    if not hasattr(timers, 'stack'):
        timers.stack = list()
        """@type: list[(logging.Logger, basestring, float, bool, int)]"""
    stack = timers.stack
    logger, name, tm_start, count_queries, queries = stack.pop()
    tm_end = time()
    logger.info(
        '%s%s took %.1fms',
        '-' * (len(stack) + 1),
        name,
        1000 * (tm_end-tm_start)
    )
    if count_queries:
        queries_end = query_count()
        logger.info('Query count: %d', queries_end-queries)
