

from django.db import transaction
from django.db import DEFAULT_DB_ALIAS
from functools import wraps
import logging
import threading


logger = logging.getLogger(__name__)
__all__ = [
    u'start_transaction',
    u'end_transaction',
    u'rollback_transaction',
    u'commit_transaction',
]
# transaction_data is a thread local data structure that will
# make sure that we are operating on the proper transaction
# stack when saving transaction depth and SIDs.  Note, that
# the limitation of this design is that you cannot use multiple
# threads to operate on a single transaction.
transaction_data = threading.local()


class HandleTransactons(object):
    def __init__(self, using):
        self.using = using
        self.function_name = None

    def __enter__(self):
        start_transaction(self.using)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_val is not None:
                logger.exception(u'Got an exception trying to execute %s; rolling back transaction: %s',
                                 self.function_name,
                                 exc_val)
                rollback_transaction(self.using)
            else:
                commit_transaction(self.using)
        finally:
            end_transaction(self.using)

    def __call__(self, func):
        @wraps(func)
        def inner(*args, ** kwargs):
            self.function_name = func.__name__
            with self:
                return func(*args, **kwargs)
        return inner


def start_transaction(using=None):
    """
    Starts transaction management in a way that is safe for nested transactions
    on platforms such as MySQL.  If the transaction depth is greater than 1, the
    start_transaction() function will use savepoints.  Otherwise, the transaction
    is treated normally.  The start_transaction() pushes the savepoint SID to a
    thread local data structure to keep track of current depth and active savepoints.
    Anytime end_transaction() is called, the most recent savepoint, if any, will
    be popped off the stack.
    @param using:  The database alias string.  The using argument defaults to None, and
    if None is provided, the function operates as if using were set to
    django.db.transaction.DEFAULT_DB_ALIAS
    @return: Nothing
    """
    if using is None:
        using = DEFAULT_DB_ALIAS
    if not hasattr(transaction_data, u'transaction_depth'):
        transaction_data.transaction_depth = dict()
    if not hasattr(transaction_data, u'sids'):
        transaction_data.sids = dict()

    transaction_depth = transaction_data.transaction_depth
    current_depth = transaction_depth.get(using, 0)
    current_depth += 1
    transaction_depth[using] = current_depth
    #logger.debug(u'Current transaction depth: %d', current_depth)
    if current_depth == 1:
        transaction.enter_transaction_management(managed=True, using=using)
        transaction.managed(flag=True, using=using)
    else:
        sid = transaction.savepoint(using=using)
        if not using in transaction_data.sids:
            transaction_data.sids[using] = list()
        transaction_data.sids[using].append(sid)


def end_transaction(using=None):
    """
    Ends transaction management for a given frame, with proper accounting
    for nesting.  This function will check the current transaction depth for
    the given using parameter.  The function will end transaction management
    if the transaction depth is 0.
    @param using: A string object for the database name.  If None is provided as
    the argument, then the using parameter defaults to transaction.DEFAULT_DB_ALIAS.
    @type using: str
    @return: None
    """
    if using is None:
        using = DEFAULT_DB_ALIAS
    if not hasattr(transaction_data, u'transaction_depth'):
        raise BaseException(u'Call to end_transaction() made without an active transaction')
    transaction_depth = transaction_data.transaction_depth
    current_depth = transaction_depth.get(using, 0)
    if current_depth == 0:
        raise BaseException(u'Call to end_transaction() made without an active transaction')
    current_depth -= 1
    if current_depth == 0:
        transaction.leave_transaction_management(using=using)
        del transaction_data.transaction_depth[using]
        if using in transaction_data.sids:
            del transaction_data.sids[using]
    else:
        transaction_depth[using] = current_depth


def rollback_transaction(using=None):
    if using is None:
        using = DEFAULT_DB_ALIAS
    transaction_depth = transaction_data.transaction_depth
    current_depth = transaction_depth.get(using, 0)
    if current_depth > 1:
        sid = transaction_data.sids[using].pop()
        transaction.savepoint_rollback(sid, using=using)
    else:
        transaction.rollback(using=using)


def commit_transaction(using=None):
    if using is None:
        using = DEFAULT_DB_ALIAS
    transaction_depth = transaction_data.transaction_depth
    current_depth = transaction_depth.get(using, 0)
    if current_depth > 1:
        sid = transaction_data.sids[using].pop()
        transaction.savepoint_commit(sid, using=using)
    else:
        transaction.commit(using=using)


def commit_on_success(using=None):
    """
    Default decorator that mimics the style of the django.db.transaction
    decorator of the same name.  Because the HandleTransactions class takes
    optional arguments, this decorator has to perform the "callable" magic
    so that the decorator operates as expected.
    @param using: The database alias associated with the function.  The function
    will default to using transaction.DEFAULT_DB_ALIAS if no value is provided.
    @return: the decorated function
    """
    if using is None:
        using = DEFAULT_DB_ALIAS
    if callable(using):
        return HandleTransactons(DEFAULT_DB_ALIAS)(using)
    return HandleTransactons(using=using)
