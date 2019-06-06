from itertools import product
from typing import List

__all__ = ['CNF', 'parse_cnf']

Clause = List[int]


class CNF:
    """
    Base class for CNF sat formulas.

    """

    def __init__(self, clauses: List[Clause], ind: List[int] = []):
        """
        Base class for CNF formulas

        Args:
            clauses: list of clauses
            ind:  Unquantified variables (ApproxMC)
        """
        # Standard
        self.clauses = clauses
        self.n = max(*(var if var > 0 else -var for clause in clauses for var in clause))
        self.m = len(clauses)

        # ApproxMC related
        self.ind = ind

    def add_clause(self, clause: Clause):
        self.clauses.append(clause)
        self.m += 1

    def evaluate(self, X: List[int]):
        """ Evaluates CNF on assignment X.

        Args:
            X: assignment of boolean variables.

        Returns:
            True if CNF evaluates to True, False otherwise.

        Examples:

             For Boolean variables x1 and x2 let's encode x1 = x2 into CNF:

             >>> clauses = [[1, -2], [-1, 2]]
             >>> cnf = CNF(clauses)

             Now let us test the truth table:
             >>> cnf.phi([0, 0])
             True
             >>> cnf.phi([1, 0 ])
             False
             >>> cnf.phi([0, 1])
             False
             >>> cnf.phi([1, 1])
             True

        """

        for clause in self.clauses:

            clause_true = False

            for var in clause:

                if var < 0 and not X[-var - 1]:
                    clause_true = True
                    break

                if var > 0 and X[var - 1]:
                    clause_true = True
                    break

            if not clause_true:
                return False

        return True

    def phi(self, X: List[int]):

        if len(self.ind) == 0:

            return self.evaluate(X)

        else:

            for s in product([0, 1], repeat=self.n - len(self.ind)):

                if self.evaluate(X + s):
                    return True

        return False

    def prob(self, X: List[int]):

        if len(self.ind) == 0:

            return .5 ** self.n

        else:

            return .5 ** (len(self.ind))

    def enumerate(self) -> List[int]:
        """ Random variable assignment.

        Yields:

            List[int]: Random assignment of Boolean variables.

        """

        if len(self.ind) == 0:

            for X in product([0, 1], repeat=self.n):
                yield X

        else:

            for X in product([0, 1], repeat=len(self.ind)):
                yield X

    def write(self, out_file: str):
        """
        Saves into ".cnf" file following the DIMACS format.

        Also, ApproxMC "c ind" lines are added at the top if ``len(ind) > 0``.

        Args:
            out_file: Address of instance file.

        Returns:
            bool: True if the CNF was saved in the input address successfully.


        Examples:

            Let us create a CNF formula of [(x1 or x2) and (not(x1) or x3)] using DIMACS' convention:

            >>> clauses = [[1, 2], [-1, 3]]
            >>> cnf = CNF(clauses)

            Now we can save this formula as 'out.cnf' as follows:

            >>> cnf.write('out.cnf')
            True

        """

        with open(out_file, 'w') as f:
            # p line
            f.write('p cnf %d %d\n' % (self.n, self.m))

            # Independent suport
            if len(self.ind) > 0:
                f.write(_ind_set(self.ind))

            # Constraints
            for clause in self.clauses:
                f.write(' '.join([str(i) for i in clause]) + ' 0\n')

        return True

    def __eq__(self, other):

        if type(self) is type(other):
            return self.__dict__ == self.__dict__
        else:
            return False


def parse_cnf(in_file: str):
    """ Reads and ".cnf" instance using the DIMACS format.

    Supports independent support for ApproxMC.

    Args:
        in_file:

    Returns:
        CNF

    Examples:

        Let us create a CNF formula of [(x1 or x2) and (not(x1) or x3)] using DIMACS' convention:

        >>> clauses = [[1, 2], [-1, 3]]
        >>> cnf1 = CNF(clauses)

        Now we can save this formula as 'out.cnf' as follows:

        >>> cnf1.write('out.cnf')
        True

        Let's read it back:

        >>> cnf2 = parse_cnf('out.cnf')
        >>> cnf1 == cnf2
        True

    """
    # Read lines
    f = open(in_file, 'r')
    lines = f.readlines()
    f.close()

    # Initializations
    clauses = []
    ind = []

    # Loop for each line
    for line in lines:

        # Check 'p' line
        if line.startswith('p'):  # Problem

            fields = line.strip().split()

            assert (fields[1] == 'cnf')

        # Read independent support line
        elif line.startswith('c ind '):

            ind.extend([int(var) for var in line.strip().split()[2:-1]])

        elif line.startswith('c'):  # Ignore comment

            pass

        else:

            clauses.append([int(var) for var in line.strip().split()[:-1]])

    return CNF(clauses, ind)


def _ind_set(ind_list):
    # signals sampling set to ApproxMC
    s = 'c ind '
    counter = 0
    for i in ind_list:
        if counter == 10:
            counter = 0
            s += '0\nc ind '
        counter += 1
        s += '%s ' % str(i)
    s += '0\n'
    return s
