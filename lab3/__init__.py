from common.sigma_matrix import SigmaMatrix
from common.berezovsky import BerezovskyMethod
from common.relation import BinRelation


def main(args):
    with open(args[0], "r", encoding="latin1") as f:
        lines = f.read().splitlines()
        matrix = [[int(n) for n in row.split()]
                  for row in lines[:20]]
    # sequence = list(reversed([int(n[1:]) for n in lines[22].split('>')]))
    # Класи впорядкованості
    matrix = [[8, 2, 5, 9],
              [5, 3, 4, 7],
              [2, 1, 4, 7],
              [3, 5, 6, 9],
              [6, 3, 4, 7]]

    class_indexes = [[0, 1], [2, 3]]

    print("Варіант №1")
    solution = BerezovskyMethod(matrix, class_indexes).solve()
    solution.render()
    print(solution.optim_domination())
