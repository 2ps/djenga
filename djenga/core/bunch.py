

__all__ = [ 'Bunch' ]


class Bunch(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def json(self):
        pass
