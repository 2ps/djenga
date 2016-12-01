from __future__ import print_function
import sys


def flush_print(st, *args, **kwargs):
    end = kwargs.pop('end', '\n')
    print(st % args, end=end)
    if sys.stdout.isatty():
        sys.stdout.flush()
