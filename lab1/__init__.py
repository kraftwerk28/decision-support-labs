#!/usr/bin/env python
from typing import List
from common.relation import BinRelation


def parse(fname: str) -> List[List[List[int]]]:
    matrices = []
    with open(fname, "r", encoding="latin1") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 7):
            matrix = [[int(n) for n in filter(len, line[:-1].split(" "))]
                      for line in lines[i: i + 7][1:]]
            matrices.append(matrix)
    return matrices


def main(args=[]):
    parsed = parse(args[0])
    for index, matrix in enumerate(parsed):
        g = BinRelation(matrix=matrix, name=f"graph{index}")
        g.render()

    # part2 = [(6, 4), (2, 3), (8, 6), (7, 1), (4, 2), (1, 4), (5, 8)]
    # part2strict = [*part2,
    #                (7, 4), (7, 2), (7, 3),
    #                (1, 3), (1, 2),
    #                (5, 6), (5, 4), (5, 2), (5, 3),
    #                (8, 4), (8, 2), (8, 3),
    #                (6, 2), (6, 3),
    #                (4, 3)]
    # part2nonstrict = [*part2strict, *[(a, a) for a in range(1, 9)]]
    # print(part2nonstrict)

    # p2 = BinRelation(pairs=part2, name="part2")
    # p2strict = BinRelation(pairs=part2strict, name="part2strict")
    # p2nonstrict = BinRelation(pairs=part2nonstrict, name="part2nonstrict")

    # p2.render()
    # p2strict.render()
    # p2nonstrict.render()

#     p3 = [*itertools.product([7, 1, 2], repeat=2),
#           *itertools.product([8, 4], repeat=2),
#           *itertools.product([6], repeat=2),
#           *itertools.product([5, 3], repeat=2)]
#     p3quasi = p3 + [(7, 8), (7, 4), (1, 8), (1, 4), (2, 8), (2, 4),
#                     (7, 6), (7, 5), (7, 3),
#                     (1, 6), (1, 5), (1, 3),
#                     (2, 6), (2, 5), (2, 3),
#                     (8, 6), (4, 6),
#                     (8, 5), (8, 3),
#                     (4, 5), (4, 3),
#                     (6, 5), (6, 3)]
#     p3weak = [*itertools.product([7, 1, 2], [8, 4]),
#               *itertools.product([7, 1, 2], [6]),
#               *itertools.product([7, 1, 2], [5, 3]),
#               *itertools.product([8, 4], [6]),
#               *itertools.product([8, 4], [5, 3]),
#               *itertools.product([6], [5, 3])]

#     p3graph = BinRelation(pairs=p3, name="part3")
#     p3graph_quasi = BinRelation(pairs=p3quasi, name="part3quasi")
#     p3graph_weak = BinRelation(pairs=p3weak, name="part3weak")

#     p3graph.render()
#     p3graph_quasi.render()
#     p3graph_weak.render()
