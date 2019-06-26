import csv


class Utf8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f):
        super(Utf8Recoder, self).__init__()
        self.reader = f

    def __iter__(self):
        return self.reader

    def next(self):
        return self.reader.next().encode('utf-8')


UnicodeCsvReader = csv.reader


def read_unicode_csv(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        reader = UnicodeCsvReader(f)
        for x in reader:
            yield x

