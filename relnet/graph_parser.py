from typing import List, Tuple


class Graph:
    """
    Base class for instances of the K-terminal reliability problem.

    This class is intended for undirected graphs. In particular, it stores the set of vertices `V`, set of edges `E`,
    terminal set `K`, and edge failure probabilities `P`.

    Attributes:
        V: List of vertices
        K: List of terminals
        E: List of edges
        P: List of edge failure probabilities


    Methods:
        write: Saves the graph object into a text readable file

    """

    def __init__(self, V: List[int], K: List[int], E: List[Tuple[int,int]], P: List[float]):
        """
        Base class for the K-terminal network reliability problem.

        Args:
            V: List of vertices
            K: List of terminals
            E: List of edges
            P: List of edge failure probabilities
        """
        self.V = V
        self.K = K
        self.E = E
        self.P = P
        self.n = len(V)  # Number of vertices
        self.m = len(E)  # Number of edges

    def write(self, out_file: str) -> bool:
        """ Writes instance file using SISRRA format for K-terminal reliability problem

            Args:
                out_file: filename to save instace.

            Returns:
                bool: True if saved successfully.

            Examples:

                Say that you have an instance of the K-terminal reliability problem:

                >>> V = [0, 1, 2, 3]
                >>> K = [0, 3]
                >>> E = [(0,1), (1,2), (2,3)]
                >>> P = [0.5] * 3
                >>> g = Graph(V, K, E, P)

                You can save at your current folder. For example:

                >>> g.write('series.txt')
                True

            """

        # Open file and write lines
        with open(out_file, 'w') as f:
            # Problem type
            f.write("p g\n")

            # Terminals
            f.write("T " + " ".join([str(i + 1) for i in self.K]) + "\n")

            # Edges
            for (i, j), p in zip(self.E, self.P):
                f.writelines("e %d %d %.12f\n" % (i + 1, j + 1, 1 - p))

        return True

    def __eq__(self, other):

        assert (isinstance(other, type(self)))

        if not self.V == other.V:
            return False

        if not self.E == other.E:
            return False

        if not self.K == other.K:
            return False

        if not self.P == other.P:
            return False

        return True


def parse_graph(in_file: str) -> Graph:
    """
    Function to parse Graph instance that has been stored using the SISRRA format.

    Args:
        in_file: path to instance file using SISRRA format.

    Returns:
        g: Graph instance.


    Examples:

        Let us first save file `series4.txt`` using method `write`:

        >>> V = [0, 1, 2, 3]
        >>> K = [0, 3]
        >>> E = [(0,1), (1,2), (2,3)]
        >>> P = [0.5] * 3
        >>> g1 = Graph(V, K, E, P)
        >>> g1.write('series4.txt')
        True

        Then, we can load the graph back from the `.txt` file:

        >>> g2 = parse_graph("series4.txt")
        >>> g1 == g2
        True

    """
    # Initialize lists
    V = []
    K = []
    E = []
    P = []

    # Open file and read lines
    f = open(in_file, 'r')
    lines = f.readlines()
    f.close()

    # Loop for each line
    for line in lines:

        # Problem type
        if line.startswith('p '):
            fields = line.strip().split(' ')[1::]
            assert (fields[0] == 'g')  # Instance file is not a Graph

        # Add edge data
        elif line.startswith('e '):
            fields = line.strip().split(' ')[1::]
            head, tail = int(fields[0]) - 1, int(fields[1]) - 1
            E.append((head, tail))
            P.append(1 - float(fields[2]))

        # Terminals
        elif line.startswith('T '):
            K.extend([int(i) - 1 for i in line.strip().split(' ')[1::]])

    # List of vertices
    V.extend(list(set([node for e in E for node in e])))

    # Graph
    g = Graph(V, K, E, P)

    return g