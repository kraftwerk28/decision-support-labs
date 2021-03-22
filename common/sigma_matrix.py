from typing import List
from .relation import BinRelation


class SigmaMatrix:
    def __init__(self, ratings: List[List[int]], vertices=None):
        self.ratings = ratings
        result = []
        for row in ratings:
            cur = []
            for row2 in ratings:
                cur.append([a - b for a, b in zip(row, row2)])
            result.append(cur)
        self.matrix = result

    def normalize(self):
        return [[[-1 if i < 0 else 1 if i > 0 else 0 for i in vec]
                 for vec in row] for row in self.matrix]

    def pareto(self):
        matrix = [[1 if all(n >= 0 for n in sigma) else 0
                   for sigma in row]
                  for row in self.matrix]
        return BinRelation(matrix=matrix)

    def majoritaric(self):
        normalized = self.normalize()
        matrix = [[1 if sum(sigma) > 0 else 0
                   for sigma in row]
                  for row in normalized]
        return BinRelation(matrix=matrix)

    def lexicographic(self, ranging):
        new_ratings = [[rating[i-1] for i in ranging]
                       for rating in self.ratings]

        def predicate(sigma):
            for i in sigma:
                if i == 0:
                    continue
                elif i == 1:
                    return True
                else:
                    return False
            return False
        normalized = SigmaMatrix(new_ratings).normalize()
        matrix = [[1 if predicate(sigma) else 0
                   for sigma in row]
                  for row in normalized]
        return BinRelation(matrix=matrix)

    def podinovsky(self):
        new_matrix = [sorted(row, reverse=True) for row in self.ratings]
        return SigmaMatrix(new_matrix).pareto()
