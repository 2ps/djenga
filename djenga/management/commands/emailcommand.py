# This file uses the following encoding:  utf-8


import logging
from django.core.management.base import BaseCommand
from commandlogginglevels import VerbosityLevels as V
import socket
from djenga.mixins.loggingmixin import LoggingMixin
from djenga.email.helpers import send_html_email


class EmailCommand(BaseCommand, LoggingMixin):
    help = u'%s%s%s%s%s' % (
        u'djenga.management.command.EmailCommand is a ',
        u'base class that provides useful functionality for ',
        u'django management commands such as logging and ',
        u'e-mail.  Subclasses should override the _handle method ',
        u'to implement actual commands.',
    )

    def _handle(self, *args, **options):
        pass

    def handle(self, *args, **options):
        self.verbosity = options.get(u'verbosity', 1)
        self.logging_level = V.to_logging_level(self.verbosity)
        return_value = self._handle(*args, **options)
        self._send_email()
        return return_value

    def _send_email(self):
        pass

    def _send_html_email(self, html_template, context, text_template=None):
        context[u'hostname'] = socket.gethostname()
        context[u'summary_messages'] = self.log_map.get(logging.INFO, [])
        context[u'info_messages'] = self.log_map.get(logging.DEBUG, [])
        context[u'warning_messages'] = self.log_map.get(logging.WARNING, [])
        context[u'error_messages'] = self.log_map.get(
            logging.ERROR, []
        ) + self.log_map.get(
            logging.CRITICAL, []
        )
        send_html_email(
            subject=u'%s' % (self.__class__.__module__,),
            template=html_template,
            context=context,
            text_template=text_template,
            inline_css=True,
        )
