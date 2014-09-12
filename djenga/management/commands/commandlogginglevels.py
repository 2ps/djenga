
#This file uses the following encoding: utf-8


import logging


__all__ = [
    u'VerbosityLevels',
    u'is_ducktyped_logger',
]

class VerbosityLevels(object):
    SUMMARY = 0
    ERROR = 1
    WARNING = 2
    INFO = 3

    VERBOSITY_TO_LOGGING = {
        SUMMARY: logging.CRITICAL,
        ERROR: logging.ERROR,
        WARNING: logging.WARNING,
        INFO: logging.DEBUG,
    }

    @staticmethod
    def to_logging_level(verbosity):
        return VerbosityLevels.VERBOSITY_TO_LOGGING.get(verbosity, logging.DEBUG)


def is_ducktyped_logger(log):
    return (hasattr(log, u'critical') and
            hasattr(log, u'error') and
            hasattr(log, u'warning') and
            hasattr(log, u'info') and
            hasattr(log, u'debug'))





