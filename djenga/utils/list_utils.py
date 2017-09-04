
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

