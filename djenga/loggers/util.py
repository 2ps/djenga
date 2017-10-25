from __future__ import absolute_import, unicode_literals, print_function
import logging
import logging.handlers
import os


__all__ = [
    'ColorFormatter',
    'BriefColorFormatter',
    'WorldWritableRotatingFileHandler',
    'IgnoreDjangoInternals',
    'IgnorePisaPdf',
    'IgnoreRequests',
    'IgnoreCaching',
]


class _Constants(object):
    LEVEL_COLORS = {
        """
        Maps a logging level to a pair of colors:
            first color is the label color
            second color is the text color
        """
        'DEBUG':    (33,  39),
        'TRACE':    (147, 153),
        'INFO':     (43,  49),
        'WARNING':  (214, 226),
        'ERROR':    (196, 197),
        'CRITICAL': (196, 197),
    }

    SHORT_LEVELS = {
        u'INFO': u'INF',
        u'WARNING': u'WRN',
        u'ERROR': u'ERR',
        u'DEBUG': u'DBG',
        u'EXCEPTION': u'EXC',
        u'CRITICAL': u'CRT'
    }

    NOT_EXTRA = {
        'args',
        'created',
        'exc_info',
        'exc_text',
        'filename',
        'funcName',
        'getMessage',
        'levelname',
        'levelno',
        'lineno',
        'message',
        'module',
        'msecs',
        'msg',
        'name',
        'pathname',
        'process',
        'processName',
        'relativeCreated',
        'thread',
        'threadName',
    }


class ColorFormatter(logging.Formatter):
    def format(self, record):
        level_colors = _Constants.LEVEL_COLORS.get(record.levelname, (33, 39))
        # setup the 256-color spectrum
        st_color   = "\033[38;5;{:d}m"
        st_reset   = "\033[0m"
        message = logging.Formatter.format(self, record)

        # Pass any simple messages from internal things,
        # like Django's runserver, without special formatting.
        if record.name == 'werkzeug' and record.levelname == 'INFO':
            # Highlight POST verbs.
            if '] "POST ' in record.message:
                record.message = record.message.replace(
                    '] "POST ',
                    '] "\033[38;5;85mPOST\033[0m ')
            return record.message
        # no highlighting for DEBUG messages
        if record.name.startswith('django.') and record.levelname == 'DEBUG':
            return record.message

        # Log entries can have data sent in the `extra` parameter;
        # e.g., when calling logger.error('msg', extra={''})
        #  Format extra to include its values in the log print.
        mp_extra = {}
        n_max = 0
        st_extra = ''
        for key in set(dir(record)) - _Constants.NOT_EXTRA:
            if key.startswith('_') or key == 'stack_info':
                continue
            mp_extra[key] = getattr(record, key)
            if len(key) > n_max:
                n_max = len(key)
        if mp_extra:
            st_extra = u'\n%s' % (u'\n'.join([
                '    {key:>{n_max}}: {value!r}'.format(
                    key=key,
                    value=value,
                    n_max=n_max
                ) for key, value in mp_extra.items()
            ]),)

        return '%s[%s/%s]%s %s%s%s' % (
            st_color.format(level_colors[0]),
            record.levelname,
            record.name,
            st_color.format(level_colors[1]),
            message,
            st_extra,
            st_reset,
        )


class BriefColorFormatter(logging.Formatter):
    def format(self, record):
        level_colors = _Constants.LEVEL_COLORS.get(record.levelname, (33, 39))
        st_color   = "\033[38;5;{:d}m"
        st_reset   = "\033[0m"
        message = logging.Formatter.format(self, record)

        # Pass any simple messages from internal things,
        # like Django's runserver, without special formatting.
        if record.name == 'werkzeug' and record.levelname == 'INFO':
            # Highlight POST verbs.
            if '] "POST ' in record.message:
                record.message = record.message.replace(
                    '] "POST ',
                    '] "\033[38;5;85mPOST\033[0m ')
            return record.message
        # no highlighting for DEBUG messages
        if record.name.startswith('django.') and record.levelname == 'DEBUG':
            return record.message

        # Log entries can have data sent in the `extra` parameter;
        # e.g., when calling logger.error('msg', extra={''})
        #  Format extra to include its values in the log print.
        mp_extra = {}
        n_max = 0
        st_extra = ''
        for key in set(dir(record)) - _Constants.NOT_EXTRA:
            if key.startswith('_') or key == 'stack_info':
                continue
            mp_extra[key] = getattr(record, key)
            if len(key) > n_max:
                n_max = len(key)
        if mp_extra:
            st_extra = u'\n%s' % (u'\n'.join([
                '    {key:>{n_max}}: {value!r}'.format(
                    key=key,
                    value=value,
                    n_max=n_max
                ) for key, value in mp_extra.items()]),)
        return u'%s[%s]%s %s%s%s' % (
            st_color.format(level_colors[0]),
            _Constants.SHORT_LEVELS.get(record.levelname, 'GEN'),
            st_color.format(level_colors[1]),
            message,
            st_extra,
            st_reset,
        )


class WorldWritableRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def _open(self):
        """Open a new log file with a more permissive umask."""
        # This is due to jobs-12 running manage.py cron jobs as a different user than what Celery runs as;
        #   otherwise we'll run into permission errors because the default RotatingFileHandler opens them
        #   as user writable, not world writable.
        old_umask = os.umask(0o111) # 666
        new_file  = logging.handlers.TimedRotatingFileHandler._open(self)
        os.umask(old_umask)
        return new_file


class IgnoreDjangoInternals(logging.Filter):
    def filter(self, record):
        if record.name.startswith('django') and record.levelname == 'DEBUG':
            return False
        return True


class IgnorePisaPdf(logging.Filter):
    def filter(self, record):
        return not (
            record.name.startswith('xhtml2pdf') and
            record.levelname == 'DEBUG'
        )


class IgnoreRequests(logging.Filter):
    def filter(self, record):
        return not (
            record.name.startswith('requests') and
            record.levelname in ('INFO', 'DEBUG')
        )


class IgnoreCaching(logging.Filter):
    def filter(self, record):
        return not (
            record.name.startswith('caching') and
            record.levelname == 'DEBUG'
        )
