
class LookupEnum(object):
    @classmethod
    def values(cls):
        if hasattr(cls, 'mp_values'):
            return cls.mp_values
        cls.mp_values = {
            key: value for key, value
            in vars(cls).items() if not key.startswith('__')
        }
        return cls.mp_values

    @classmethod
    def value(cls, n_id):
        return cls.values().get(n_id)


class ReversibleEnum(object):
    @classmethod
    def codes(cls):
        if hasattr(cls, 'mp_codes'):
            return cls.mp_codes
        cls.mp_codes = {
            value: key for key, value
            in vars(cls).items() if not key.startswith('__')
        }
        return cls.mp_codes

    @classmethod
    def code(cls, n_id):
        return cls.codes().get(n_id)
