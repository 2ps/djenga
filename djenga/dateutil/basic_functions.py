
# encoding: utf-8


from __future__ import unicode_literals
import logging
from datetime import date


logger = logging.getLogger(__name__)
__all__ = [
    u'unpack_date',
    u'bump',
    u'bump_down',
]


def unpack_date(d=None):
    """
    _unpack_date is a quick utility function that
    takes a date and unpacks it to its day, month and
    year values.

    @param d the date to be unpacked.  If no date is
    passed in, then today's date is unpacked.

    @return a tuple with day, month and year (in that order)
    """
    if not d:
        d = date.today()
    return d.day, d.month, d.year


def bump(month, year):
    """
    bump is a utility function that takes a given month
    and year and returns the next month and year.  For
    example bump(1, 2014) would return (2, 2014) while
    bump(12, 2013) would return (1, 2014).

    @param month the month to be bumped
    @param year the year to be bumped

    @return a tuple with the next month and year in that order
    """
    month = month % 12 + 1
    if month == 1:
        year += 1
    return month, year


def bump_down(month, year):
    """
    bump is a utility function that takes a given month
    and year and returns the next month and year.  For
    example bump(1, 2014) would return (2, 2014) while
    bump(12, 2013) would return (1, 2014).

    @param month the month to be bumped
    @param year the year to be bumped

    @return a tuple with the next month and year in that order
    """
    month -= 1
    if month == 0:
        year -= 1
        month = 12
    return month, year
