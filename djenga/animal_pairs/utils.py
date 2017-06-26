
from .dictionary import ADJECTIVES, ANIMALS
import random


__all__ = [ 'animal_pair' ]


def animal_pair():
    return u'%s-%s' % (
        random.choice(ADJECTIVES),
        random.choice(ANIMALS),
    )
