# encoding: utf-8


import threading
from time import time
from django.db import connection


timers = threading.local()


def start_timer(logger, name, count_queries=False):
    """
    @type logger: logging.Logger | accounting.management.commands.accountingcommand.Command
    @type name: basestring
    @type count_queries: bool
    """
    if not hasattr(timers, u'stack'):
        timers.stack = list()
        """@type: list[(logging.Logger, basestring, float, bool, int)]"""
    stack = timers.stack
    tm_start = time()
    stack.append((logger, name, tm_start, count_queries, len(connection.queries)))
    logger.info(u'%sStarting %s', u'-' * len(stack), name)


def end_timer():
    if not hasattr(timers, u'stack'):
        timers.stack = list()
        """@type: list[(logging.Logger, basestring, float, bool, int)]"""
    stack = timers.stack
    logger, name, tm_start, count_queries, queries = stack.pop()
    tm_end = time()
    logger.info(
        u'%s%s took %.1fms',
        u'-' * (len(stack) + 1),
        name,
        1000 * (tm_end-tm_start)
    )
    if count_queries:
        queries_end = len(connection.queries)
        logger.info(u'Query count: %d', queries_end-queries)
