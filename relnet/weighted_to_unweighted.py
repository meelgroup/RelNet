from typing import List, Union

from numpy import isclose
from relnet.graph_parser import Graph

__all__ = ['weighted2unweighted']


def weighted2unweighted(g: Graph) -> Graph:
    """ Transforms weighted graph `g` into unweighted graph `ug`.

    Uses series-parallel reductions.

    Args:
        g: Weighted graph

    Returns:
        ug: Unweighted graph

    """
    vertex_counter = g.n
    E_new = []

    for i in range(g.m):
        if 1 - g.P[i] > 0:
            b = float2bin(1 - g.P[i])
            head, tail = g.E[i]
            e_new, vertex_counter = _weighted_edge(b, head, tail, vertex_counter)
            E_new.extend(e_new)

    V_new = list(range(vertex_counter))
    P_new = [0.5] * len(E_new)
    ug = Graph(V_new, g.K, E_new, P_new)

    return ug


def _weighted_edge(b, head=0, tail=1, vertex_counter=0):
    """Details as in paper [PDMV-2019]"""
    # Parameters
    z = [head]
    for bit in b:
        if bit == 0:
            vertex_counter += 1

            if vertex_counter == tail:
                vertex_counter += 1

            z.append(vertex_counter)

        else:
            z.append(z[-1])

    def _eta(k):
        if b[k - 1]:
            return z[k - 1], tail
        else:
            return z[k - 1], z[k]

    return [_eta(k) for k in range(1, len(b) + 1)], vertex_counter


def float2bin(p: float, min_bits: int = 10, max_bits: int = 20, relative_error_tol=1e-02) -> List[bool]:
    """ Converts probability `p` into binary list `b`.

    Args:
        p: probability such that 0 < p < 1
        min_bits: minimum number of bits before testing relative error.
        max_bits: maximum number of bits for truncation.
        relative_error_tol: relative error tolerance

    Returns:
        b: List[bool]

    Examples:

        Probability 0.5 becomes:

        >>> float2bin(0.5)  # Is 0.1
        [1]

        Moreover 0.125 is:
        >>> float2bin(0.125)  # Is 0.001
        [0, 0, 1]

        Some numbers get truncated. For example, probability 1/3 becomes:
        >>> float2bin(1/3)  # Is 0.0101010101...
        [0, 1, 0, 1, 0, 1, 0, 1, 0]

        You can increase the maximum number of bits to reach float precision, for example:
        >>> 1/3
        0.3333333333333333
        >>> q = float2bin(1/3, 64)
        >>> bin2float(q)
        0.3333333333333333
        >>> 1/3 == bin2float(q)
        True

    """

    assert 1 > p > 0
    b = []
    i = 1
    original_p = 1 - p

    while p != 0 or i > max_bits:
        if i > min_bits:
            if isclose(1 - bin2float(b), original_p, rtol=relative_error_tol, atol=0):
                break
        if p >= 2 ** -i:
            b.append(True)
            p -= 2 ** -i
        else:
            b.append(False)

        i += 1

    return b


def bin2float(q) -> float:
    """
    Converts binary list 'q' into a probability 0 < p < 1.

    Args:
        q: List[Union[0,1]]

    Returns:

    """

    n = len(q)
    p = 0
    for i in range(n):
        p += q[i] * 2 ** -(i + 1)

    return p
