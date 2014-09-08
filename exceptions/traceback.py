# encoding: utf-8
# pylint: disable=pointless-string-statement

from __future__ import unicode_literals
import sys


class FullTraceback(object):
    def __init__(self, tb_frame, tb_lineno, tb_next):
        self.tb_frame = tb_frame
        self.tb_lineno = tb_lineno
        self.tb_next = tb_next


def current_stack(skip=0):
    p_frame = None
    try:
        1/0
    except ZeroDivisionError:
        p_frame = sys.exc_info()[2].tb_frame

    for _ in xrange(skip + 2):
        p_frame = p_frame.f_back
    rg_frames = []
    while p_frame is not None:
        rg_frames.append((p_frame, p_frame.f_lineno))
        p_frame = p_frame.f_back
    return rg_frames


def extend_traceback(tb, stack, n_max=6):
    """
    This function "extends" a traceback by filling in
    actual stack frames into the traceback.  This is useful
    for debugging and for using the full traceback with
    Sentry
    """
    p_head = tb
    for x, (tb_frame, tb_lineno) in enumerate(stack):
        if x >= n_max:
            break
        p_head = FullTraceback(tb_frame, tb_lineno, p_head)
    return p_head


def full_exc_info():
    """
    This function is designed to mimic sys.exc_info.
    However, unlike sys.exc_info, the `full_exc_info`
    function returns the full traceback.
    """
    t, v, p_traceback = sys.exc_info()
    p_full = extend_traceback(p_traceback, current_stack(1))
    return t, v, p_full