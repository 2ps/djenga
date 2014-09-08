
# encoding: utf-8


from __future__ import unicode_literals
from decimal import Decimal
from decimal import ROUND_FLOOR
from decimal import ROUND_DOWN
from decimal import ROUND_UP


__all__ = [
    u'currency_round_down',
    u'currency_round_up',
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

