# encoding: utf-8


from __future__ import unicode_literals
import logging
import codecs
import sys
from traceback import format_exc
from django.conf import settings
from django.core.management.base import OutputWrapper


class LoggingMixin(object):
    verbosity = 3 if settings.DEBUG else 1
    """@type: int"""
    indent = 0
    """@type: int"""
    logging_level = logging.DEBUG if settings.DEBUG else 1
    log_map = dict()
    logging_initialized = False
    print_level = True

    def set_verbosity(self, verbosity):
        LEVELS = {
            0: logging.CRITICAL,
            1: logging.ERROR,
            2: logging.WARNING,
            3: logging.DEBUG,
        }
        self.verbosity = verbosity
        self.logging_level = LEVELS[verbosity]

    def initialize_logging(self):
        if not self.logging_initialized:
            try:
                self.stdout = OutputWrapper(self.stdout._out, ending='')
            except AttributeError:
                self.stdout = OutputWrapper(sys.stdout, ending='')
            # self.stdout = codecs.getwriter('utf8')(self.stdout)
            self.logging_initialized = True

    def color_format(self, level, message):
        level_colors = {
            # Level and a pair of colors: first for the label, the rest for the text;
            #   the bolder color label can make them easier to spot in the console log.
            logging.DEBUG:        ( 33,  39),
            # logging.TRACE:        (147, 153),
            logging.INFO:         ( 43,  49),
            logging.WARNING:      (214, 226),
            logging.ERROR:        (196, 197),
            logging.CRITICAL:     (196, 197),
        }.get(level, (33, 39))
        color   = "\033[38;5;{:d}m"         # 256-color to give wider spectrum than just ANSI
        reset   = "\033[0m"

        # Pass any simple messages from internal things, like Django's runserver, without special formatting.
        mp_levels = {
            logging.INFO: u'INF',
            logging.WARNING: u'WRN',
            logging.ERROR: u'ERR',
            logging.DEBUG: u'DBG',
            logging.CRITICAL: u'CRT'
        }
        st_level = mp_levels[level]
        level_prefix = '%s[%s] ' % (color.format(level_colors[0]), st_level)
        return u'{level_prefix}{color_normal}{message}{reset}'.format(
            level_prefix    = level_prefix if self.print_level else '',
            message         = message,
            color_normal    = color.format(level_colors[1]),
            reset           = reset
        )

    def llog(self, logging_level, format_string, *args):
        """
        @param logging_level:
            50 = summary/critical
            40 = error
            30 = warning
            20 = info
            10 = debug
        @return:
        """
        LEVELS = {
            logging.CRITICAL,
            logging.ERROR,
            logging.WARNING,
            logging.INFO,
            logging.DEBUG
        }
        if logging_level not in LEVELS:
            logging_level = logging.DEBUG
        message = format_string % args
        if logging_level >= self.logging_level:
            if hasattr(self, 'stdout'):
                self.initialize_logging()
                self.stdout.write(u' ' * self.indent)
                if self.stdout.isatty():
                    self.stdout.write(self.color_format(logging_level, message))
                else:
                    self.stdout.write(message)
                self.stdout.write('\n')
                self.log_map.setdefault(logging_level, []).append(message)

    def log(self, format_string, *args):
        message = format_string % args
        if hasattr(self, 'stdout'):
            self.initialize_logging()
            self.stdout.write(u' ' * self.indent)
            self.stdout.write(message)
            self.stdout.write('\n')

    def critical(self, format_string, *args):
        self.llog(logging.CRITICAL, format_string, *args)

    def debug(self, format_string, *args):
        self.llog(logging.DEBUG, format_string, *args)

    def info(self, format_string, *args):
        self.llog(logging.INFO, format_string, *args)

    def warning(self, format_string, *args):
        self.llog(logging.WARNING, format_string, *args)

    def error(self, format_string, *args):
        self.llog(logging.ERROR, format_string, *args)

    def exception(self, format_string, *args):
        p_type, p_exception, _ = sys.exc_info()
        self.llog(logging.ERROR, format_string, *args)
        self.llog(logging.ERROR, u'Exception message: %s', p_exception)
        self.llog(logging.ERROR, u'Exception type   : %s', p_type)
        self.llog(logging.ERROR, u'Traceback\n%s', format_exc())
