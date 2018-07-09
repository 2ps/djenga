"""
This module provides functions for rounding numbers as currency.

>>> currency_round_down(1.9999)
Decimal('1.99')
>>> currency_round_up(1.9911)
Decimal('2.00')
>>> currency_round_up4(1.9911)
Decimal('1.9912')
>>> currency_round_half_up(1.9951)
Decimal('2.00')
>>> currency_round_half_up4(1.995555)
Decimal('1.9956')
"""

# encoding: utf-8


from __future__ import unicode_literals
from decimal import Decimal
from decimal import ROUND_FLOOR
from decimal import ROUND_DOWN
from decimal import ROUND_UP
from decimal import ROUND_HALF_UP
from typing import TypeVar


__all__ = [
    'currency_round_down',
    'currency_round_up',
    'currency_round_up4',
    'currency_round_half_up',
    'currency_round_half_up4',
    'round_up',
    'round_down',
    'round_half_up',
    'round_floor',
]


def currency_round_down(amount):
    """
    Useful helper function that takes a numerical amount, converts
    it to a decimal.Decimal object and rounds it down to the nearest
    cent.
    """
    amount = amount or 0.00
    amount = Decimal(amount)
    amount = amount.quantize(Decimal(u'.0001'), rounding=ROUND_FLOOR)
    amount = amount.quantize(Decimal(u'.01'), rounding=ROUND_DOWN)
    return amount


def currency_round_up(amount):
    """
    Useful helper function that takes a numerical amount, converts
    it to a decimal.Decimal object and rounds it up to the nearest
    cent.
    """
    amount = amount or 0.00
    amount = Decimal(amount)
    amount = amount.quantize(Decimal(u'.0001'), rounding=ROUND_FLOOR)
    amount = amount.quantize(Decimal(u'.01'), rounding=ROUND_UP)
    return amount


def currency_round_up4(amount):
    """
    Useful helper function that takes a numerical amount, converts
    it to a decimal.Decimal object and rounds it up to the nearest
    one-hundredth of a cent.
    """
    amount = amount or 0.00
    amount = Decimal(amount)
    amount = amount.quantize(Decimal(u'.0001'), rounding=ROUND_UP)
    return amount


def currency_round_half_up(amount):
    """
    Useful helper function that takes a numerical amount, converts
    it to a decimal.Decimal object and rounds it up to the nearest
    cent using half-adjust rounding.  Unlike `currency_round_up`, this
    function will use half-adjust rounding for the cents place after
    floor rounding the ten thousandths place.
    """
    amount = amount or 0.00
    amount = Decimal(amount)
    amount = amount.quantize(Decimal(u'.0001'), rounding=ROUND_FLOOR)
    amount = amount.quantize(Decimal(u'.01'), rounding=ROUND_HALF_UP)
    return amount


def currency_round_half_up4(amount):
    """
    Useful helper function that takes a numerical amount, converts
    it to a decimal.Decimal object and rounds it up to the nearest
    one-hundredth of a cent using half-adjust rounding.  Unlike
    `currency_round_up4`, this function will use half-adjust rounding
    for the ten thousandths place.
    """
    amount = amount or 0.00
    amount = Decimal(amount)
    amount = amount.quantize(Decimal(u'.0001'), rounding=ROUND_HALF_UP)
    return amount


DecimalLike = TypeVar('DecimalLike', str, float, Decimal)


def q_round(
        amount: DecimalLike,
        places: int=2,
        rounding=ROUND_HALF_UP) -> Decimal:
    """
    Useful helper function that takes a numerical amount, converts
    it to a decimal.Decimal object and rounds it up to the nearest
    one-hundredth of a cent using half-adjust rounding.  Unlike
    `currency_round_up4`, this function will use half-adjust rounding
    for the ten thousandths place.
    """
    amount = amount or Decimal(0.00)
    if not isinstance(amount, Decimal):
        amount = Decimal(amount)
    # This version is slower according to timeit
    # q = Decimal('1') / Decimal(10 ** places)
    # This version, using strings, is actually faster
    if places > 0:
        q = '.%s1' % ('0' * (places - 1),)
    else:
        q = '1'
    q = Decimal(q)
    amount = amount.quantize(q, rounding=rounding)
    return amount


def round_up(amount: DecimalLike, places: int=2) -> Decimal:
    """
    Rounds amount up, to a specified number of places
    :type amount: float | str | decimal.Decimal
    :type places: int
    :rtype: Decimal
    >>> round_up(1.241, 1)
    Decimal('1.3')
    """
    return q_round(amount, places, ROUND_UP)


def round_down(amount, places=2):
    """
    Rounds amount down, to a specified number of places
    :type amount: float | str | decimal.Decimal
    :type places: int
    :rtype: Decimal
    >>> round_down(1.995555, 4)
    Decimal('1.9955')
    >>> round_down('58.12', 0)
    Decimal('58')
    """
    return q_round(amount, places, ROUND_DOWN)


def round_floor(amount: DecimalLike, places: int=2) -> Decimal:
    """
    Floor rounds amount to a specified number of places
    :type amount: float | str | decimal.Decimal
    :type places: int
    :rtype: Decimal
    >>> round_floor(1.995555, 4)
    Decimal('1.9955')
    >>> round_floor('58.12', 0)
    Decimal('58')
    """
    return q_round(amount, places, ROUND_FLOOR)


def round_half_up(amount: DecimalLike, places: int=2) -> Decimal:
    """
    Rounds amount, to a specified number of places, using half-rounding
    :type amount: float | str | decimal.Decimal
    :type places: int
    :rtype: Decimal
    Decimal('1.9956')
    >>> round_half_up(1.9911, 3)
    Decimal('1.991')
    >>> round_half_up(1.995, 2)
    Decimal('2.00')
    """
    return q_round(amount, places, ROUND_HALF_UP)
