import os
import json
import yaml


class ConfigurationMixin(object):
    """
    Enhances a django management command by allowing it to
    read from a configuration file at the beginning of its
    run and exposing the loaded configuration in an
    instance member called `config`.  The default
    configuration file may be specified in a class member
    called `config_file`.  This default configuration file
    may be overridden at the command line by using the
    `--config` or `-c` option.

    n.b. This mixin requires that any sub-classes making use of
    it to call super(ClassName, self).add_arguments(parser)
    at the beginning of any override of the `add_arguments`
    method.
    """
    config_file = None

    def __init__(self):
        super(ConfigurationMixin, self).__init__()
        self.config = {}

    def add_arguments(self, parser):
        """
        :type parser: argparse.ArgumentParser
        """
        super(ConfigurationMixin, self).add_arguments(parser)
        parser.add_argument(
            '-c', '--config',
            dest='config_file',
            default=self.config_file,
            help='the /path/to the configuration file')

    def load_config(self):
        if not self.config_file:
            return
        _, ext = os.path.splitext(self.config_file)
        loader = json
        if ext in ('.yml', '.yaml'):
            loader = yaml
        with open(self.config_file, 'r') as f:
            self.config = loader.load(f)

    def execute(self, *args, **options):
        self.config_file = options.get('config_file')
        self.load_config()
        super(ConfigurationMixin, self).execute(*args, **options)
