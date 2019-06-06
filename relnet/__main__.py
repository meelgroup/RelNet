import sys

from relnet import parse_graph, krelnet, count


def main():
    in_file, out_file = sys.argv[1:3]
    g = parse_graph(in_file)
    cnf = krelnet(g)
    if cnf.write(out_file):
        print('[relnet] CNF file "{}" saved\n'
              '[relnet] Number of sampling variables is {}'.format(out_file, len(cnf.ind), out_file))

    if len(sys.argv) > 3 and bool(sys.argv[3]):
        if len(sys.argv) == 5:
            epsilon = float(sys.argv[4])
            delta = float(sys.argv[5])
            count(out_file, epsilon, delta)
        else:
            count(out_file)
    else:
        print('[relnet] For counting issue:\n'
              '         $  approxmc {}'.format(out_file))


if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[0] == "-h":
        print("USAGE: python -m relnet <inputGraph> <outputCNF>")
        print("USAGE (with ApproxMC installed): python -m relnet <inputGraph> <outputCNF> 1 <epsilon> <delta>")
        exit(-1)
    main()
