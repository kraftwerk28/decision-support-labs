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
            vertices = sorted(set([p[0] for p in pairs] +
                                  [p[1] for p in pairs]))
            matrix = [[0] * len(vertices) for _ in range(len(vertices))]
            for a, b in pairs:
                i, j = vertices.index(a), vertices.index(b)
                matrix[i][j] = 1
            self.matrix = matrix
            self.pairs = pairs
            self.vertices = vertices
        else:
            raise Exception("Either matrix or pairs must be provided")
        self.graph = Digraph(format="png")
        for tail, row in zip(string.ascii_uppercase, self.matrix):
            for head, connected in zip(string.ascii_uppercase, row):
                if connected:
                    self.graph.edge(tail, head)

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
    # for index, matrix in list(enumerate(parsed))[1:2]:
    for index, matrix in enumerate(parsed):
        g = BinRelation(matrix=matrix, name=f"graph{index}")
        g.render()
        print("Властивості:", ", ".join(g.relation_properties()))
        print("Класи бін. відношень:",
              ", ".join(g.relation_classes()) or "немає")
        print("\n")
