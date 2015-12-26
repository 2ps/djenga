
import importlib


def get_function(name):
    """
    Loads a function by its fully qualified name.  Examples:
    `get_function('datetime.datetime')`
    `get_function('djenga.reflection.get_function')`

    :param name: the fully-qualified function name
    :type name: str | unicode
    :return: the function requested
    :rtype: function | class
    """
    if name in locals():
        return locals()[name]
    if name in globals():
        return globals()[name]
    st_module, st_function = name.rsplit('.', 1)
    module = importlib.import_module(st_module)
    return getattr(module, st_function, None)
