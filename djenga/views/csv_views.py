import csv
from django.http import HttpResponse
from django.views.generic import View


class CsvView(View):
    """
    This class offers several utility functions to
    make it easier to return a CSV response to a user.
    To use:
        1.  Sub-class this class
        2.  Call self.initialize_response with a proposed download filename
        3.  write data to the CSV response with self.writerow
        4.  return self.response from the get or post function to send the
            CSV to the user
    """
    def __init__(self, **kwargs):
        super(CsvView, self).__init__(**kwargs)
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
        self.writer = csv.writer(self.response)

    def writerow(self, data):
        self.writer.writerow(data)


