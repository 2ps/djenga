import json
import logging
from unittest import mock
from django.test import TestCase
from djenga.logging.formatters import JsonFormatter, JsonTaskFormatter


__all__ = [ 'JsonFormatterTest', ]
log = logging.getLogger(__name__)


class JsonFormatterTest(TestCase):
    def test_json_formatter(self):
        formatter = JsonFormatter()
        with self.assertLogs(log) as log_context:
            for handler in log.handlers:
                handler.setFormatter(formatter)
            log.info('Hello, Gwenna!', extra={'favorite': 'Olive'})
            data = log_context.output[-1]
            data = json.loads(data)
            self.assertIn('timestamp', data)
            self.assertEqual(data['message'], 'Hello, Gwenna!')
            self.assertEqual(data['logger'],
                             'djenga_tests.tests.json_formatters')
            self.assertEqual(data['favorite'], 'Olive')
            try:
                raise ValueError('test exception')
            except ValueError as ex:
                log.exception('%s', ex)
                data = log_context.output[-1]
                data = json.loads(data)
                self.assertEqual(data['exception_type'], 'builtins.ValueError')
                self.assertIn('test exception', data['message'])
                self.assertEquals('test exception', data['exception_args'][0])

    class MockTask:
        class MockRequest:
            id = 'olive'
        request = MockRequest()
        name = 'gwenna'

    @mock.patch('celery._state.get_current_task',
                return_value=MockTask())
    def test_task_formatter(self, mock_current_task):
        formatter = JsonTaskFormatter()
        with self.assertLogs(log) as log_context:
            for handler in log.handlers:
                handler.setFormatter(formatter)
            log.info('Hello, Olive!')
            data = log_context.output[-1]
            data = json.loads(data)
            self.assertEqual(data['task_id'], 'olive')
            self.assertEqual(data['task_name'], 'gwenna')
