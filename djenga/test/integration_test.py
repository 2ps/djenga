import inspect
import yaml
from time import time
from djenga.utils import flush_print
from djenga.utils.print_utils import dot_leader


class IntegrationTestException(Exception):
    pass


class IntegrationTest(object):
    """
    Subclass this class to use for running integration
    tests with the IntegrationTestCommand.  In order
    to use this class, a subclass should define one or
    more instance member functions that begin with the
    word `test` and takes no arguments other than self.
    These functions will be called in alphabetical order
    by the super classes `run_test` function.  Example:

    from djenga.test import IntegrationTest

    class MyIntegrationTest(IntegrationTest):
        def test_addition(self):
            x = 1
            self.assert_equal(x, 1)
            x += 4
            self.assert_equal(x, 5)

    An integration test can also access YAML or JSON test
    data from a file specified by the class variable
    `test_data_file`.  This test data will is made
    available to the sub class through `self.test_data`.
    Example:
        In a file called path/to/my_test_data.yml

        ---
        step_1: 1
        step_2: 5

        In the integration test file:

        class MyIntegrationTest(IntegrationTest):
            test_data_file = 'path/to/my_test_data.yml'

            def test_addition(self):
                x = 1
                self.assert_equal(
                    x, self.test_data['step_1'],
                    'Oh no! failed step 1')
                x += 4
                self.assert_equal(
                    x, self.test_data['step_2'],
                    'Oh no! failed step 2')
    """
    test_data_file = ''

    def __init__(self):
        self.test_data = None
        self.load_test_data()

    def load_test_data(self):
        if not self.test_data_file:
            return
        with open(self.test_data_file, 'r') as f:
            self.test_data = yaml.load(f)

    def assert_true(self, value, message=''):
        if value is not True:
            raise IntegrationTestException(
                message or f'failure: [{value}] was not true')

    def assert_truthy(self, value, message=''):
        if value:
            raise IntegrationTestException(
                message or f'failure: [{value}] was not truthy')

    def assert_false(self, value, message=''):
        if value is not False:
            raise IntegrationTestException(
                message or f'failure: [{value}] was true')

    def assert_falsey(self, value, message=''):
        if value:
            raise IntegrationTestException(
                message or f'failure: [{value}] was not falsey')

    def asset_greater_than(self, left, right, message=''):
        if left <= right:
            raise IntegrationTestException(
                message or f'failure: [{left}] <= [{right}]')

    def asset_greater_than_equal(self, left, right, message=''):
        if left <= right:
            raise IntegrationTestException(
                message or f'failure: [{left}] > [{right}]')

    def assert_less_than(self, left, right, message=''):
        if left >= right:
            raise IntegrationTestException(
                message or f'failure: [{left}] >= [{right}]')

    def assert_less_than_equal(self, left, right, message=''):
        if left > right:
            raise IntegrationTestException(
                message or f'failure: [{left}] > [{right}]')

    def assert_equal(self, left, right, message=''):
        if left != right:
            raise IntegrationTestException(
                message or 'failure: [%s] != [%s]' % (left, right))

    def assert_not_equal(self, left, right, message=''):
        if left == right:
            raise IntegrationTestException(
                message or 'failure: [%s] == [%s]' % (left, right))

    def run_test(self):
        test_methods = [
            value
            for key, value in inspect.getmembers(self)
            if key.startswith('test') and callable(value)
        ]
        test_methods.sort(key=lambda fn: fn.__name__)
        all_passed = True
        for x in test_methods:
            dot_leader('%s.%s', self.__class__.__name__, x.__name__, end='')
            tm_start = time()
            status = 'passed'
            units = 's'
            try:
                x()
            except IntegrationTestException as ex:
                status = 'failed (%s)' % (ex,)
                all_passed = False
            finally:
                tm_total = time() - tm_start
            if tm_total < 1:
                tm_total *= 1000
                units = 'ms'
            flush_print('%s %.1f%s', status, tm_total, units)
        return all_passed
