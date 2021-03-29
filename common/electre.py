from typing import List
from .relation import BinRelation


class ElectreAlgorithm:
    def __init__(self, ratings: List[List[int]], weights: List[float]):
        self.ratings = ratings
        self.weights = weights

    def solve(self):
        weights_matrix = [[sum(weight
                               for weight, a, b
                               in zip(self.weights, row, other_row)
                               if a >= b)
                           for other_row in self.ratings]
                          for row in self.ratings]
        print('\n'.join(str(row) for row in weights_matrix))
