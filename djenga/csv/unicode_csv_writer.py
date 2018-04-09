# encoding: utf-8

import csv
import six
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


class UnicodeCsvWriter(object):
    def __init__(self, f, dialect=csv.excel, **kwds):
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f

    def writerow(self, row):
        """
        writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        """
        if six.PY3:
            self.writer.writerow([s.encode('utf-8') for s in row ])
        else:
            self.writer.writerow([
                s.encode('utf-8') for s in row if isinstance(s, unicode)
            ])
        data = self.queue.getvalue()
        data = data.decode('utf-8')
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
