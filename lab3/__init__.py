from common.sigma_matrix import SigmaMatrix
from common.berezovsky import BerezovskyMethod
from common.relation import BinRelation


def write_solution(filename, matrix, sequence, class_indexes):
    sm = SigmaMatrix(matrix)
    pareto = sm.pareto()
    majority = sm.majoritaric()
    lex = sm.lexicographic(sequence)
    berezovsky = BerezovskyMethod(matrix, class_indexes).solve()
    podinovsky = sm.podinovsky()
    with open(filename, "w") as f:
        f.write("1\n")
        f.write(pareto.raw_matrix())
        f.write("2\n")
        f.write(majority.raw_matrix())
        f.write("3\n")
        f.write(lex.raw_matrix())
        f.write("4\n")
        f.write(berezovsky.raw_matrix())
        f.write("5\n")
        f.write(podinovsky.raw_matrix())


def main(args):
    with open(args[0], "r", encoding="latin1") as f:
        lines = f.read().splitlines()
        matrix = [[int(n) for n in row.split()]
                  for row in lines[:20]]
    sequence = list([int(n[1:]) for n in lines[22].split('>')])
    # Класи впорядкованості
    class_indexes = [[int(n[1:]) for n in cl.strip('{} ').split(',')]
                     for cl in lines[-1].split('<')]
    write_solution("lab3/solution.txt", matrix, sequence, class_indexes)
