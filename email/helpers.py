# This python file uses the following encoding: utf-8
# pylint: disable=pointless-string-statement


import logging
import os
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from settings import DJENGA_FROM_EMAIL
from settings import DJENGA_DEFAULT_RECIPIENTS
import inlinecss

logger = logging.getLogger(__name__)


__all__ = [
    u'send_email',
    u'send_html_email',
]


def send_email(sender, recipients, subject, body):
    try:
        sender = sender or DJENGA_FROM_EMAIL
        recipients = recipients or DJENGA_DEFAULT_RECIPIENTS
        msg = EmailMultiAlternatives(subject, body, sender, recipients)
        msg.send()
    except BaseException, ex: # pylint:disable=broad-except
        logger.exception(u'Exception encountered trying to send error e-mail:  %s', ex)


def send_html_email(subject, template, context,
                    text_template=None, text_body=None,
                    sender=None, recipients=None, cc=None, bcc=None,
                    inline_css=True,):
    """
    Sends an HTML e-mail and a text counterpart using Django's EmailMultiAlternatives
    class.
    @param subject: the subject line for the e-mail
    @type subject: unicode
    @param template: the django template that will be used to generate the
    HTML portion of the e-mail.
    @type template: basestring
    @param context: the context dictionary that will be used to render
    the HTML template
    @type context: dict[basestring, object]
    @param text_body: the text alternative for those e-mail clients that
    cannot view the HTML.
    @type text_body: basestring
    @param recipients: the recipients to whom the e-mail will be sent.
    If no recipients are specified, a default set of e-mails are used.
    @type: list[basestring]
    """
    html_body = loader.render_to_string(template, context)
    if inline_css:
        html_body = inlinecss.from_string(html_body, logger, )
    if text_body is None:
        if text_template is None:
            text_body = '<no text>'
        else:
            text_body = loader.render_to_string(text_template, context)
            # See https://code.djangoproject.com/ticket/2594
            text_body = os.linesep.join([s for s in text_body.splitlines() if s.strip()])
    sender = sender or DJENGA_FROM_EMAIL
    recipients = recipients or DJENGA_DEFAULT_RECIPIENTS
    try:
        msg = EmailMultiAlternatives(
            subject,
            text_body,
            sender,
            recipients,
            cc=cc,
            bcc=bcc
        )
        msg.attach_alternative(html_body, u'text/html')
        msg.send()
    except BaseException, ex: # pylint: disable=broad-except
        logger.exception(u'Exception encountered trying to send e-mail:  %s', ex)


