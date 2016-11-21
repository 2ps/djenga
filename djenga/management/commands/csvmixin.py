import codecs
from djenga.csv import UnicodeCsvWriter


class CsvMixin(object):
    """
    Enhances a django management command by allowing it to
    write to a CSV file through an
    instance function called `writerow`.  The output file
    may be specified at the command line by using the
    `--output` or `-o` option.  If no output file is specified,
    the command will output to stdout.

    n.b. This mixin requires that any sub-classes making use of
    it to call super(ClassName, self).add_arguments(parser)
    at the beginning of any override of the `add_arguments`
    method.
    """
    output_file = None

    def __init__(self):
        super(CsvMixin, self).__init__()
        self.csv_writer = None
        """@type: UnicodeCsvWriter"""
        self.file_handle = None
        """@type: stream"""

    def add_arguments(self, parser):
        """
        Adds the output file argument to the list of
        arguments accepted by the command
        :type parser: argparse.ArgumentParser
        """
        super(CsvMixin, self).add_arguments(parser)
        parser.add_argument(
            '-o', '--output',
            dest='output_file',
            help='The /path/to/output-file.csv of the output CSV.'
                 '  If no output file is specified, the command'
                 ' will output the CSV contents to stdout.')

    def get_csv_writer(self):
        """
        Returns an initialized CSV writer
        :rtype: UnicodeCsvWriter
        """
        if not self.csv_writer:
            if self.output_file:
                self.file_handle = codecs.open(self.output_file, 'w', encoding='utf-8')
            else:
                self.file_handle = self.stdout
            self.csv_writer = UnicodeCsvWriter(self.file_handle)
        return self.csv_writer

    def writerow(self, data):
        """
        Writes a row of data to the CSV
        :param data: a row of data to be written
        """
        self.get_csv_writer().writerow(data)

    def close_file_handle(self):
        """
        Closes any initialized file handles
        """
        if self.file_handle and self.output_file:
            self.file_handle.close()

    def execute(self, *args, **options):
        """
        Override the execute function so that we
        can get a handle on the output_file argument
        and close the file handle gracefully after command
        exit.
        """
        self.output_file = options.get('output_file')
        try:
            super(CsvMixin, self).execute(*args, **options)
        finally:
            self.close_file_handle()
