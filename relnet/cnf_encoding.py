from relnet.graph_parser import Graph
from relnet.cnf_parser import CNF
from relnet.weighted_to_unweighted import weighted2unweighted

__all__ = ['krelnet']


def krelnet(g: Graph):
    """ Returns SAT encoding of :class:`relnet.graph_parser.Graph`.


    Args:
        g: Graph instance.

    Returns:
        CNF: SAT encoding as CNF

    Examples:

        Let's import a grid instance for the all-terminal reliability problem

        >>> from netrel import *
        >>> from netrel.generators import grid_m_n_k
        >>> g = grid_m_n_k(3, 3, 0.5)
        >>> 1-brute_force(g)
        0.894775390625

        Now let us encode this instance as a model counting problem:

        >>> cnf = relnet(g)
        >>> brute_force(cnf)
        0.894775390625


    """

    # (I) WEIGHTED TO UNWEIGHTED
    g = weighted2unweighted(g)

    # (II) SAT encoding
    # initializations
    clauses = []
    ind = []

    # Size of IS
    size_is = g.m

    # (II-a) CONSTRAINTS

    # Node marking constraints
    if len(g.K) == 2:
        clauses.append([g.K[0] + 1 + size_is])
        clauses.append([-(g.K[1] + 1 + size_is)])
    else:
        clauses.append([(i + 1 + size_is) for i in g.K])
        clauses.append([-(i + 1 + size_is) for i in g.K])

    # Transitivity constraint
    for i in range(g.m):
        # unpack nodes
        u, v = g.E[i]
        u += 1 + size_is
        v += 1 + size_is

        # edge
        uv = i + 1

        # Push clauses
        clauses.append([-u, -uv, v])
        clauses.append([u, -uv, -v])

    # (II-b) INDEPENDENT SUPPORT

    ind += list(range(1, size_is + 1))

    return CNF(clauses, ind)

