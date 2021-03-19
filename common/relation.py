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


def zipEnum(*args):
    for i, t in enumerate(zip(*args)):
        yield tuple([i, *t])


def from_pairs(pairs):
    """Construct 2D matrix from list of pairs"""
    vertices = sorted(set([p[0] for p in pairs] +
                          [p[1] for p in pairs]))
    matrix = [[0 for _ in vertices] for _ in vertices]
    for a, b in pairs:
        i, j = vertices.index(a), vertices.index(b)
        matrix[i][j] = 1
    return matrix


def from_matrix(matrix, vertices=None):
    """Construct list of pairs from 2D matrix"""
    assert all(len(row) == len(matrix) for row in matrix), "Invalid matrix"
    if vertices is None:
        vertices = list(string.ascii_uppercase[:len(matrix)])
    return [(a, b)
            for row, a in zip(matrix, vertices)
            for c, b in zip(row, vertices)
            if c]


class BinRelation:
    PROP_NAMES = set(name
                     for name_tup in RELATION_CLASSES.values()
                     for name in name_tup)

    def __init__(self, matrix=None, pairs=None, name="graph", vertices=None):
        self.name = name
        if matrix is not None:
            self.vertices = (vertices or
                             list(string.ascii_uppercase[:len(matrix)]))
            self.matrix = matrix
            self.pairs = from_matrix(matrix, vertices=self.vertices)
        elif pairs is not None:
            self.vertices = vertices or sorted(set([p[0] for p in pairs] +
                                                   [p[1] for p in pairs]))
            self.pairs = pairs
            self.matrix = from_pairs(pairs)
        else:
            raise Exception("Either matrix or pairs must be provided")
        self.graph = Digraph(format="png")
        for a, b in self.pairs:
            self.graph.edge(str(a), str(b))

    def __getitem__(self, pair):
        return self.matrix[pair[0]][pair[1]]

    def __str__(self):
        mtx_body = "\n".join(" ".join(str(n) for n in [self.vertices[i], *row])
                             for i, row in enumerate(self.matrix))
        header = " ".join([" ", *(str(v) for v in self.vertices)])
        mtx_str = f"{header}\n{mtx_body}"
        pairs_str = ", ".join(f"({a} {b})" for a, b in self.pairs)
        return "\n".join([f"{self.name}:", pairs_str, mtx_str])

    @staticmethod
    def from_assos_tuples(*args):
        tuples = []
        myargs = list(args)
        while myargs:
            a, b = myargs.pop(0), myargs.pop(0)
            tuples.append((a, b))
        pairs = [(t[0], x) for t in tuples for x in t[1]]
        return BinRelation(pairs=pairs)

    def render(self):
        self.graph.render(self.name, cleanup=True)
        print(str(self))
        # Display picture in terminal
        name = f"{self.name}.png"
        try:
            os.system(f"kitty +kitten icat {name}")
            os.remove(name)
        except Exception as e:
            print(e)

        print("Властивості:", ", ".join(self.relation_properties()))
        print("Класи бін. відношень:",
              ", ".join(self.relation_classes()) or "немає")
        print()

    # Properties
    def reflexive(self) -> bool:
        return all(self[i, i] > 0 for i, _ in enumerate(self.vertices))

    def antireflexive(self) -> bool:
        return all(self[i, i] == 0 for i, _ in enumerate(self.vertices))

    def symmetric(self) -> bool:
        s = len(self.vertices)
        for i in range(s):
            for j in range(i+1, s):
                if self[i, j] != self[j, i]:
                    return False
        return True

    def asymmetric(self) -> bool:
        s = len(self.vertices)
        for i in range(s):
            for j in range(i, s):
                if self[i, j] and self[j, i]:
                    return False
        return True

    def antisymmetric(self) -> bool:
        s = len(self.vertices)
        for i in range(s):
            for j in range(i+1, s):
                if self[i, j] and self[j, i]:
                    return False
        return True

    def transitive(self) -> bool:
        for pair1 in self.pairs:
            outgoing = filter(lambda x: x[0] == pair1[1], self.pairs)
            for pair2 in outgoing:
                if (pair1[0], pair2[1]) not in self.pairs:
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

    def has_cycle(self) -> bool:
        for start_vertex in self.vertices:
            visited, on_stack = set(), set()
            stack = [start_vertex]
            while stack:
                cur = stack[-1]
                if cur in visited:
                    if cur in on_stack:
                        on_stack.remove(cur)
                    stack.pop()
                else:
                    visited.add(cur)
                    on_stack.add(cur)
                children = [b for a, b in self.pairs if a == cur]
                for child in children:
                    if child not in visited:
                        stack.append(child)
                    elif child in on_stack:
                        return True
        return False

    def x_star_p(self):
        """X*p"""
        return [v for i, v, row in zipEnum(self.vertices, self.matrix)
                if all(c == 0 if i == j else c > 0 for j, c in enumerate(row))]

    def x_star_r(self):
        """X*r, max element"""
        return [v for v, row in zip(self.vertices, self.matrix)
                if all(c > 0 for c in row)]

    def x_star_star_r(self):
        """X**r, strict max"""
        return [v for i, v, row in zipEnum(self.vertices, self.matrix)
                if all(c > 0 for c in row)
                and all(row[i] == 0 for j, row in enumerate(self.matrix)
                        if j != i)]

    def x_zero_p(self):
        """X⁰p"""
        return [v for i, v in enumerate(self.vertices)
                if all(row[i] == 0 for row in self.matrix)]

    def x_zero_r(self):
        """X⁰r"""
        return [v for i, v in enumerate(self.vertices)
                if all(row[i] == 0 or (self[i, j] and self[j, i])
                       for j, row in enumerate(self.matrix))]

    def x_zero_zero_r(self):
        """X⁰⁰r"""
        return [v for i, v in enumerate(self.vertices)
                if all(row[i] == 0 or (row[i] > 0 and i == j)
                       for j, row in enumerate(self.matrix))]

    def optim_domination(self):
        if self.asymmetric():
            return self.x_star_p()
        else:
            best = self.x_star_r() + self.x_star_star_r()
            return list(set(best))

    def optim_blocking(self):
        if self.asymmetric():
            return self.x_zero_p()
        else:
            best = self.x_zero_r() + self.x_zero_zero_r()
            return list(set(best))

    def build_C0(self):
        """Neumann–Morgenstern algorithm"""
        if self.has_cycle():
            return []
        # All vertex "parents":
        parents = {x: [a for a, b in self.pairs if b == x]
                   for x in self.vertices}
        current_s = set(self.x_zero_p())  # S₀
        accum_s = current_s.copy()  # Si
        current_q = current_s.copy()  # Q₀
        while True:
            if not current_s:
                break
            next_s = [a for a, b in parents.items()
                      if all(v in accum_s for v in b)
                      and a not in accum_s]
            next_q = [v for v in next_s
                      if all(u not in current_q for u in parents[v])]
            current_s = next_s
            accum_s.update(current_s)
            current_q.update(next_q)
        result = list(current_q)
        assert self.optimal_by_NM(result)  # Verification
        return result

    def prove_inter_stability(self, vertices):
        for v in vertices:
            parents = [a for a, b in self.pairs if b == v]
            if any(p in vertices for p in parents):
                return False
        return True

    def prove_outer_stability(self, vertices):
        for v in (v for v in self.vertices if v not in vertices):
            pairs = [(a, v) for a in vertices]
            if not any(pair in self.pairs for pair in pairs):
                return False
        return True

    def optimal_by_NM(self, vertices):
        return (self.prove_inter_stability(vertices)
                and self.prove_outer_stability(vertices))
