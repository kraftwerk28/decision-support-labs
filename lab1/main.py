#!/usr/bin/env python
import sys
import os
from typing import List
from graphviz import Digraph
import string
import itertools

RELATION_CLASSES = {
    "equivalent": ("reflexive", "symmetric", "transitive"),
    "strict_order": ("antireflexive", "asymmetric", "transitive"),
    "nonstrict_order": ("reflexive", "antisymmetric", "transitive"),
    "quasi_order": ("reflexive", "transitive"),
    "weak_ordered": ("asymmetric", "transitive", "negative_transitive"),
    "tolerant": ("reflexive", "symmetric"),
}


class BinRelation:
    PROP_NAMES = set(name
                     for name_tup in RELATION_CLASSES.values()
                     for name in name_tup)

    def __init__(self, matrix=None, pairs=None, name="graph"):
        self.name = name
        if matrix is not None:
            pairs = []
            for row, a in zip(matrix, string.ascii_uppercase):
                for conn, b in zip(row, string.ascii_uppercase):
                    if conn:
                        pairs.append((a, b))
            self.pairs = pairs
            self.matrix = matrix
            self.vertices = list(string.ascii_uppercase[:len(matrix)])
        elif pairs is not None:
            vertices = sorted(set([str(p[0]) for p in pairs] +
                                  [str(p[1]) for p in pairs]))
            matrix = [[0] * len(vertices) for _ in range(len(vertices))]
            for a, b in pairs:
                i, j = vertices.index(str(a)), vertices.index(str(b))
                matrix[i][j] = 1
            self.matrix = matrix
            self.pairs = pairs
            self.vertices = vertices
        else:
            raise Exception("Either matrix or pairs must be provided")
        self.graph = Digraph(format="png")
        for a, b in self.pairs:
            self.graph.edge(str(a), str(b))

    def __str__(self):
        mtx_str = "\n".join(" ".join(str(n) for n in [self.vertices[i], *row])
                            for i, row in enumerate(self.matrix))
        mtx_str = " ".join([" ", *self.vertices]) + "\n" + mtx_str
        pairs_str = ", ".join(f"({a} {b})" for a, b in self.pairs)
        return "\n".join([f"{self.name}:", pairs_str, mtx_str])

    def render(self):
        self.graph.render(self.name, cleanup=True)
        print(str(self))
        # Display picture in terminal
        try:
            os.system(f"kitty +kitten icat {self.name}.png")
        except:
            pass

        print("Властивості:", ", ".join(self.relation_properties()))
        print("Класи бін. відношень:",
              ", ".join(self.relation_classes()) or "немає")
        print("\n")

    # Properties
    def reflexive(self) -> bool:
        return all(self.matrix[i][i] for i in range(len(self.vertices)))

    def antireflexive(self) -> bool:
        return all(not self.matrix[i][i] for i in range(len(self.vertices)))

    def symmetric(self) -> bool:
        s = len(self.vertices)
        for row in range(s):
            for col in range(s):
                if self.matrix[row][col] and not self.matrix[col][row]:
                    return False
        return True

    def asymmetric(self) -> bool:
        s = len(self.vertices)
        for row in range(s):
            for col in range(s):
                if self.matrix[row][col] and self.matrix[col][row]:
                    return False
        return True

    def antisymmetric(self) -> bool:
        s = len(self.vertices)
        for row in range(s):
            for col in range(s):
                if row == col:
                    continue
                if self.matrix[row][col] and self.matrix[col][row]:
                    return False
        return True

    def transitive(self) -> bool:
        for pair1 in self.pairs:
            outgoing = filter(lambda x: x[0] == pair1[1], self.pairs)
            for pair2 in outgoing:
                connected = (p for p in self.pairs
                             if p[0] == pair1[0] and p[1] == pair2[1])
                if not next(connected, None):
                    return False
        return True

    def negative_transitive(self) -> bool:
        for pair1 in self.pairs:
            non_outgoing = filter(lambda x: x[0] != pair1[1], self.pairs)
            for pair2 in non_outgoing:
                connected = (p for p in self.pairs
                             if p[0] == pair1[0] and p[1] == pair2[1])
                if next(connected, None):
                    return False
        return True

    def complete(self) -> bool:
        return all(p in self.vertices
                   for p in itertools.permutations(self.vertices, 2))

    def connected(self) -> bool:
        return all((a, b) in self.vertices or (b, a) in self.vertices
                   for a, b in itertools.product(self.vertices, repeat=2))

    def weakly_connected(self) -> bool:
        return all((a, b) in self.vertices or (b, a) in self.vertices
                   for a, b in itertools.permutations(self.vertices, r=2))

    def relation_properties(self) -> List[str]:
        return [name for name in self.PROP_NAMES if getattr(self, name)()]

    def relation_classes(self) -> List[str]:
        properties = self.relation_properties()
        return [klass for klass, props in RELATION_CLASSES.items()
                if set(props).issubset(properties)]


def parse(fname: str) -> List[List[List[int]]]:
    matrices = []
    with open(fname, "r", encoding="latin1") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 7):
            matrix = [[int(n) for n in filter(len, line[:-1].split(" "))]
                      for line in lines[i: i + 7][1:]]
            matrices.append(matrix)
    return matrices


if __name__ == "__main__":
    parsed = parse(sys.argv[1])
    for index, matrix in enumerate(parsed):
        g = BinRelation(matrix=matrix, name=f"graph{index}")
        g.render()

    part2 = [(6, 4), (2, 3), (8, 6), (7, 1), (4, 2), (1, 4), (5, 8)]
    part2strict = [*part2,
                   (7, 4), (7, 2), (7, 3),
                   (1, 3), (1, 2),
                   (5, 6), (5, 4), (5, 2), (5, 3),
                   (8, 4), (8, 2), (8, 3),
                   (6, 2), (6, 3),
                   (4, 3)]
    part2nonstrict = [*part2strict, *[(a, a) for a in range(1, 9)]]
    print(part2nonstrict)

    p2 = BinRelation(pairs=part2, name="part2")
    p2strict = BinRelation(pairs=part2strict, name="part2strict")
    p2nonstrict = BinRelation(pairs=part2nonstrict, name="part2nonstrict")

    p2.render()
    p2strict.render()
    p2nonstrict.render()
