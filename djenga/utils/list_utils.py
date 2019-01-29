from typing import Iterable


__all__ = [
    'chunkify',
    'chunkify_iterable',
]


def chunkify(rg, n_max=1000):
    """
    generates sublists of at most n_max
    elements from the provided array
    :param rg: list
    :param n_max: the maximum sublist length
    :return:
    """
    m, n_len = 0, len(rg)
    while m < n_len:
        l, m = m, m + n_max
        yield rg[l:m]


def chunkify_iterable(what: Iterable, n_max: int = 1000):
    """
    generates sublists of at most n_max
    elements from the provided iterable
    """
    n_max = n_max or 1000
    chunk = []
    for x in what:
        chunk.append(x)
        if len(chunk) == n_max:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

