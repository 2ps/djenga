import os
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from StringIO import StringIO
from djenga.csv import UnicodeCsvWriter
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.views.generic import View


class CsvViewMixin(object):
    """
    This class offers several utility functions to
    make it easier to return a CSV response to a user.
    To use:
        1.  Add this class as a mixin to any class-based view
        2.  Call self.initialize_response with a proposed download filename
        3.  write data to the CSV response with self.writerow
        4.  return self.response from the get or post function to send the
            CSV to the user
    """
    def __init__(self, **kwargs):
        super(CsvViewMixin, self).__init__(**kwargs)
        self.response = None
        """:type HttpResponse"""
        self.writer = None
        """:type csv.writer"""

    def initialize_response(self, filename):
        """
        Prepares the HttpResponse that will be used
        to contain the CSV data
        :param filename: the default filename for the user
        when he/she downloads the file.
        """
        self.response = HttpResponse(content_type='text/csv')
        self.response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        self.writer = UnicodeCsvWriter(self.response)

    def writerow(self, data):
        self.writer.writerow(data)


class CsvView(CsvViewMixin, View):
    """
    A helper class so that you can just subclass from
    CsvView directly instead of using the mixin.
    """
    pass


class ZippedCsvMixin(object):
    """
    This mixin offers several utility functions to
    make it easier to return a CSV response to a user.
    To use:
        1.  Add this class as a mixin
        2.  Call self.initialize_response with a proposed download filename
        3.  write data to the CSV response with self.writerow
        4.  call self.finalize_response to finalize the response
        4.  return self.response from the get or post function to send the
            CSV to the user
    """
    def __init__(self, **kwargs):
        super(ZippedCsvMixin, self).__init__(**kwargs)
        self.response = None
        """:type HttpResponse"""
        self.writer = None
        """:type csv.writer"""
        self.csv_buffer = StringIO()
        self.zip_buffer = BytesIO()
        self.filename = None
        self.archive = None
        self.response = None

    def initialize_response(self, filename):
        """
        Prepares the HttpResponse that will be used
        to contain the CSV data
        :param filename: the default filename for the user
        when he/she downloads the file.
        """
        self.writer = UnicodeCsvWriter(self.csv_buffer)
        self.filename = filename
        self.archive = ZipFile(self.zip_buffer, 'w', compression=ZIP_DEFLATED)

    def finalize_response(self):
        self.archive.writestr(self.filename, self.csv_buffer.getvalue().encode('utf-8'))
        self.archive.close()
        _, ext = os.path.splitext(self.filename)
        self.response = StreamingHttpResponse(FileWrapper(self.zip_buffer), content_type='application/zip')
        self.response['Content-Disposition'] = 'attachment; filename="%s"' % self.filename.replace(ext, '.zip')
        self.response['Content-Length'] = self.zip_buffer.tell()
        self.zip_buffer.seek(0)

    def writerow(self, data):
        self.writer.writerow(data)


class ZippedCsvView(ZippedCsvMixin, View):
    """
    A helper class so that you can just subclass from
    ZippedCsvView directly instead of using the mixin.
    """
    pass
