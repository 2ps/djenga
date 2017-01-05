import codecs
import csv
# from django.core.management.base import BaseCommand


class InputCsvMixin(object):
    """
    Enhances a django management command by allowing it to
    read from an input CSV file through an
    instance function called `read_input`.  The input file
    may be specified at the command line by using the
    `--input` or `-i` option.

    n.b. This mixin requires that any sub-classes making use of
    it to call super(ClassName, self).add_arguments(parser)
    at the beginning of any override of the `add_arguments`
    method.
    """
    def __init__(self):
        super(InputCsvMixin, self).__init__()
        self.input_rows = []
        """@type: list[list]"""
        self.header = []
        """@type: list[str]"""
        self.input_file_help = 'the /path/to the input CSV file'
        """@type: str"""
        self.input_filename = None
        """@type: str"""

    def add_arguments(self, parser):
        """
        Adds the input file argument to the option
        parser
        :param parser: argparse.Parser
        """
        super(InputCsvMixin, self).add_arguments(parser)
        parser.add_argument(
            '-i', '--input',
            dest='input_file',
            required=True,
            help=self.input_file_help,
        )

    def read_input(self):
        """
        Reads the input file specified by the user into the
        `self.header` and `self.input_rows` instance variables.
        :return:
        """
        with codecs.open(self.input_filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            self.header = reader.next()
            self.input_rows = [ x for x in reader ]

    def read_input_as_dict(self):
        """
        Reads the input file specified by the user
        into the `self.input_rows` instance variable
        as a series of dicts using csv.DictWriter
        :return:
        """
        with codecs.open(self.input_filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.input_rows = [ x for x in reader ]

    def execute(self, *args, **options):
        """
        Overrides the `BaseCommand.execute` method to allow
        us to grab the input filename argument from
        the parser and store it into `self.input_filename`
        :param args:
        :param options:
        :return:
        """
        self.input_filename = options['input_file']
        return super(InputCsvMixin, self).execute(*args, **options)
