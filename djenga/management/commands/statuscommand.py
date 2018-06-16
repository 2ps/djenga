# encoding: utf-8


from __future__ import unicode_literals
import logging
import codecs
import sys
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections
from django.utils import timezone
from djenga.models import ManagementCommand
from djenga.models import CommandOutput


class StatusCommand(BaseCommand):
    def set_verbosity(self, verbosity):
        LEVELS = {
            0: logging.CRITICAL,
            1: logging.ERROR,
            2: logging.WARNING,
            3: logging.DEBUG,
        }
        self.verbosity = verbosity
        self.logging_level = LEVELS[verbosity]

    def create_parser(self, prog_name, subcommand):
        parser = super(StatusCommand, self).create_parser(prog_name, subcommand)
        parser.add_argument(
            '--last',
            action='store_true',
            dest='b_show_last',
            default=False
        )
        return parser

    def start_run(self):
        ManagementCommand.objects.update_or_create(
            name=self.command_name,
            defaults={
                'last_run': datetime.now(timezone.utc),
                'task_status': 'running',
            }
        )

    @property
    def command_name(self):
        name = self.__module__
        return name.replace('.management.commands', '')

    def end_run(self, success=True):
        if self.current_line:
            self.plain_log('\n')
        connection = connections['default']
        if connection.connection and not connection.is_usable():
            connection.close()
        q = ManagementCommand.objects.get(
            name=self.command_name,
        )
        q.status = 'success' if success else 'error'
        if success:
            q.last_success = datetime.now(timezone.utc)
        q.save()
        CommandOutput.objects.create(
            command=q,
            output='\n'.join(self.output)
        )

    def __init__(self):
        super(StatusCommand, self).__init__()
        self.verbosity = 3 if settings.DEBUG else 1
        """@type: int"""
        self.indent = 0
        """@type: int"""
        self.logging_level = logging.DEBUG if settings.DEBUG else 1
        self.output = []
        self.print_level = True
        self.stdout.ending = ''
        self.stdout = codecs.getwriter('utf8')(self.stdout)
        self.current_line = ''

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
            if self.stdout.isatty():
                message = self.color_format(logging_level, message)
                self.stdout.write(message)
            else:
                self.stdout.write(message)
            self.stdout.write('\n')
            self.add_message(message)

    def add_message(self, message):
        if self.current_line:
            self.output.append((self.current_line + message).strip())
            self.current_line = ''
        elif message is not None:
            self.output.append(message.strip())

    def log(self, format_string, *args):
        message = format_string % args
        self.stdout.write(message)
        self.stdout.write('\n')
        self.add_message(message)

    def color_log(self, fn, format_string, *args):
        message = format_string % args
        if message[-1] == '\n':
            close_line = True
            message = message[:-1]
        else:
            close_line = False
        message = fn(message)
        self.stdout.write(message)
        if close_line:
            self.stdout.write('\n')
            self.add_message(message)
        elif self.current_line:
            self.current_line += message
        else:
            self.current_line = message

    def plain_log(self, format_string, *args):
        self.color_log(lambda x: x, format_string, *args)

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
        p_type, p_exception, p_traceback = sys.exc_info()
        self.llog(logging.ERROR, format_string, *args)
        self.llog(logging.ERROR, u'Exception message: %s', p_exception)
        self.llog(logging.ERROR, u'Exception type   : %s', p_type)
        self.llog(logging.ERROR, u'Traceback\n%s', p_traceback.format_exc())

    def show_last(self):
        try:
            p = CommandOutput.objects.filter(
                command__name=self.command_name
            ).latest('id')
            self.log('%s', p.output)
        except CommandOutput.DoesNotExist:
            self.log('This is the first run of %s', self.command_name)

    def execute(self, *args, **options):
        if options.get('b_show_last', False):
            self.show_last()
            return
        success = False
        try:
            self.start_run()
            super(StatusCommand, self).execute(*args, **options)
            success = True
        except:
            success = False
            raise
        finally:
            self.end_run(success)
