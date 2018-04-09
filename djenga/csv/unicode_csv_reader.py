import codecs
import csv
import six


class Utf8Recoder(object):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f):
        super(Utf8Recoder, self).__init__()
        self.reader = f

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode('utf-8')


if six.PY2:
    class UnicodeCsvReader(object):
        """
        A CSV reader which will iterate over lines in the CSV file "f",
        which is encoded in the given encoding.
        """
        def __init__(self, f, dialect=csv.excel, **kwargs):
            super(UnicodeCsvReader, self).__init__()
            f = Utf8Recoder(f)
            self.reader = csv.reader(f, dialect=dialect, **kwargs)

        def next(self):
            row = next(self.reader)
            return [ unicode(s, 'utf-8') for s in row ]

        def __iter__(self):
            return self

    def read_unicode_csv(filename, encoding='utf-8'):
        with codecs.open(filename, 'r', encoding=encoding) as f:
            reader = UnicodeCsvReader(f)
            for x in reader:
                yield x

elif six.PY3:
    UnicodeCsvReader = csv.reader

    def read_unicode_csv(filename, encoding='utf-8'):
        with open(filename, 'r', encoding=encoding) as f:
            reader = UnicodeCsvReader(f)
            for x in reader:
                yield x

