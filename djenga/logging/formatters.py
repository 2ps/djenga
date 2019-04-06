from datetime import datetime
import json
import logging


__all__ = [
    'JsonFormatter',
    'JsonTaskFormatter',
]


class JsonFormatter(logging.Formatter):
    """
    This formatter is useful if you want to ship logs to a
    json-based centralized log aggregation platform like ELK.
    n.b., this formatter is very opinionated.
    """
    def format_message(self, record: logging.LogRecord):  # noqa: C901
        s = record.getMessage()
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != '\n':
                s = s + '\n'
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != '\n':
                s = s + '\n'
            s = s + self.formatStack(record.stack_info)
        return s

    def iso_time(self, record: logging.LogRecord):
        dt = datetime.utcfromtimestamp(record.created)
        return dt.isoformat('T')

    DEFAULT_KEYS = {
        'name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename',
        'module', 'exc_info', 'exc_text', 'stack_info', 'lineno', 'funcName',
        'created', 'msecs', 'relativeCreated', 'thread', 'threadName',
        'processName', 'process',
    }

    def to_dict(self, record: logging.LogRecord):
        data = {
            'timestamp': self.iso_time(record),
            'message': self.format_message(record),
            'function': record.funcName,
            'path': record.pathname,
            'module': record.module,
            'level': record.levelname,
            'line_number': record.lineno,
        }
        for key, value in record.__dict__.items():
            if key not in JsonFormatter.DEFAULT_KEYS:
                data[key] = value
        return data

    def format(self, record: logging.LogRecord):
        return json.dumps(self.to_dict(record))


class JsonTaskFormatter(JsonFormatter):
    """
    This formatter is useful if you want to ship logs to a
    json-based centralized log aggregation platform like ELK.
    n.b., this formatter is very opinionated.
    """
    def to_dict(self, record: logging.LogRecord):
        data = super(JsonTaskFormatter, self).to_dict(record)
        try:
            from celery._state import get_current_task
            task = get_current_task()
            if task and task.request:
                data['task_id'] = task.request.id
                data['task_name'] = task.name
        except ImportError:
            pass
        return data
