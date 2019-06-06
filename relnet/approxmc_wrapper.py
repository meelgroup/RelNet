import os


solver_path = '/usr/local/bin/approxmc'


__all__ = ['count']


def count(cnf_file: str, epsilon=0.8, delta=0.2):

    temp_file = '.{}.tmp'.format(cnf_file)

    os.system('{0} --epsilon {2} --delta {3} {1} > {4}'.format(solver_path, cnf_file, epsilon, delta, temp_file))

    with open(temp_file, 'r') as f:
        lines = f.readlines()
        print("".join(lines[-2:])[:-1])

    os.remove(temp_file)

    return True
