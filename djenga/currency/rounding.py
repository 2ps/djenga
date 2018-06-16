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


__all__ = [
    u'currency_round_down',
    u'currency_round_up',
    u'currency_round_up4',
    u'currency_round_half_up',
    u'currency_round_half_up4',
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
