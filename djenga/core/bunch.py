

__all__ = [ 'Bunch' ]


class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def json(self):
        pass
