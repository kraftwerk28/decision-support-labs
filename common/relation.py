import os
from typing import List
import string
import itertools
from graphviz import Digraph

RELATION_CLASSES = {
    "equivalent": ("reflexive", "symmetric", "transitive"),
    "strict_order": ("antireflexive", "asymmetric", "transitive"),
    "nonstrict_order": ("reflexive", "antisymmetric", "transitive"),
    "quasi_order": ("reflexive", "transitive"),
    "weak_ordered": ("asymmetric", "negative_transitive"),
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
        for a, b in self.pairs:
            self.graph.edge(str(a), str(b))

    def __str__(self):
        mtx_body = "\n".join(" ".join(str(n) for n in [self.vertices[i], *row])
                             for i, row in enumerate(self.matrix))
        header = " ".join([" ", *(str(v) for v in self.vertices)])
        mtx_str = f"{header}\n{mtx_body}"
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
        print()

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

    def find_cycle(self) -> List[str]:
        colors = {c: 0 for c in self.vertices}  # 0: white; 1: grey; 2: black

        def dfs(v, path):
            if colors[v] == 1:
                return path
            colors[v] = 1
            for a, b in filter(lambda x: x[0] == v, self.pairs):
                if next_vert := dfs(b, path + [b]):
                    return next_vert
            colors[v] = 2
            return []
        fst = self.vertices[0]
        return dfs(fst, [fst])
