# This file uses the following encoding:  utf-8


import logging
from django.core.management.base import BaseCommand
from commandlogginglevels import VerbosityLevels as V
import socket
from settings import DJENGA_FROM_EMAIL


class EmailCommand(BaseCommand):
    help = u'%s%s%s%s%s' % (
        u'djenga.management.command.EmailCommand is a ',
        u'base class that provides useful functionality for ',
        u'django management commands such as logging and ',
        u'e-mail.  Subclasses should override the _handle method ',
        u'to implement actual commands.',
    )

    verbosity = 1
    indent = 0
    logging_level = logging.ERROR
    summary_messages = None
    error_messages = None
    warning_messages = None
    info_messages = None
    log_map = None

    def _handle(self, *args, **options):
        pass

    def handle(self, *args, **options):
        self.verbosity = options.get(u'verbosity', 1)
        self.logging_level = V.to_logging_level(self.verbosity)
        self._initialize_super()
        return_value = self._handle(*args, **options)
        self._send_email()
        return return_value

    def _format(self, level, message):
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
        return u'{color_bold}[{level}]{color_normal} {message}{reset}'.format(
            level           = mp_levels.get(level, u'GEN'),
            message         = message,
            color_bold      = color.format(level_colors[0]),
            color_normal    = color.format(level_colors[1]),
            reset           = reset
        )

    def _log(self, logging_level, format_string, *args):
        """
        @param logging_level:
            50 = summary/critical
            40 = error
            30 = warning
            20 = info
            10 = debug
        @return:
        """
        if not logging_level in self.log_map:
            logging_level = logging.DEBUG
        message = format_string % args
        if logging_level >= self.logging_level:
            self.stdout.write(u' ' * self.indent)
            self.stdout.write(self._format(logging_level, message))
            self.stdout.write(u'\n')
            self.log_map[logging_level].append(message)

    def critical(self, format_string, *args):
        self._log(logging.CRITICAL, format_string, *args)

    def debug(self, format_string, *args):
        self._log(logging.DEBUG, format_string, *args)

    def info(self, format_string, *args):
        self._log(logging.INFO, format_string, *args)

    def warning(self, format_string, *args):
        self._log(logging.WARNING, format_string, *args)

    def error(self, format_string, *args):
        self._log(logging.ERROR, format_string, *args)

    def exception(self, format_string, *args):
        import sys
        p_type, p_exception, p_traceback = sys.exc_info()
        self._log(logging.ERROR, format_string, *args)
        self._log(logging.ERROR, u'Exception message: %s', p_exception)
        self._log(logging.ERROR, u'Exception type   : %s', p_type)
        self._log(logging.error, u'Traceback\n%s', p_traceback.format_exc())

    def _send_email(self):
        pass

    def _initialize_super(self):
        self.summary_messages = list()
        self.info_messages = list()
        self.warning_messages = list()
        self.error_messages = list()
        self.log_map = {
            logging.CRITICAL: self.summary_messages,
            logging.WARNING: self.warning_messages,
            logging.INFO: self.info_messages,
            logging.DEBUG: self.info_messages,
            logging.ERROR: self.error_messages,
        }

    def _send_html_email(self, html_template, context, text_template=None):
        context[u'hostname'] = socket.gethostname()
        context[u'summary_messages'] = self.summary_messages
        context[u'info_messages'] = self.info_messages
        context[u'warning_messages'] = self.warning_messages
        context[u'error_messages'] = self.error_messages
        send_html_email(
            subject=u'A/R:  %s' % (self.__class__.__module__,),
            template=html_template,
            context=context,
            text_template=text_template,
            inline_css=True,
        )
