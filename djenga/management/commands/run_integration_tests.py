import inspect
import os
import sys
from importlib import import_module
from django.conf import settings
from django.core.management.base import BaseCommand
from djenga.test import IntegrationTest
from djenga.mixins import LoggingMixin
from djenga.utils.print_utils import dot_lead


class Command(LoggingMixin, BaseCommand):
    """
    The IntegrationTestCommand is a mangement command
    that will run all classes in any INSTALLED_APP's
    `integration_test` submodule or the specified module
    so long as the class is a subclass of
    `djenga.test.IntegrationTest`.
    """
    help = (
        'run_integration_tests is a management command '
        "that will run all classes in any INSTALLED_APP's "
        '`integration_tests` submodule or the specified module '
        'so long as the class is a subclass of '
        '`djenga.test.IntegrationTest`.')

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(stdout, stderr, no_color)
        self.modules = None
        """@type: list[str] list of dot delimited modules in which to look for tests"""
        self.tests = None
        """@type: list[str] list of class names of specific tests wanted to be run"""

    def create_parser(self, prog_name, subcommand):
        parser = super(Command, self).create_parser(prog_name, subcommand)
        parser.add_argument(
            '--module', '-m',
            action='append',
            dest='modules',
            help='specifies a dotted module path in which '
                 'one or more `IntegrationTest` subclasses '
                 'can be found and run')
        parser.add_argument(
            '--test', '-t',
            action='append',
            dest='tests',
            help='specifies the name of '
                 'one or more `IntegrationTest` subclasses '
                 'to be run')
        return parser

    def check_module(self, module, display_warnings=True):
        exists = os.path.exists('%s/__init__.py' % module.replace('.', '/'))
        try:
            import_module(module)
            return True
        except ImportError:
            if display_warnings or exists:
                self.warning('WARNING: could not import module [%s]', module)
            return False

    def set_modules(self, modules):
        display_warnings = False
        if modules:
            display_warnings = True
        else:
            modules = [
                '%s.integration_tests' % x
                for x in settings.INSTALLED_APPS ]
        self.modules = [
            x for x in modules
            if self.check_module(x, display_warnings) ]

    def set_tests(self, tests):
        self.tests = []
        for module in self.modules:
            self.info(dot_lead('Checking %s for tests', module))
            module = import_module(module)
            for name, klass in inspect.getmembers(module):
                if name.startswith('__') or not inspect.isclass(klass): continue
                x = klass()
                if isinstance(x, IntegrationTest) and (
                    not tests or
                    klass.__name__ in tests
                ):
                    self.info(dot_lead('  + loaded %s', klass.__name__))
                    self.tests.append(x)

    def run_tests(self):
        all_passed = True
        for x in self.tests:
            status = x.run_test()
            all_passed = status and all_passed
        return all_passed

    def handle(self, *args, **options):
        self.set_modules(options.get('modules'))
        self.set_tests(options.get('tests'))
        success = self.run_tests()
        if not success:
            sys.exit(1)
