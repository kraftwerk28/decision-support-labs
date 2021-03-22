from .sigma_matrix import SigmaMatrix
from .relation import BinRelation


class BerezovskyMethod:
    def __init__(self, ratings, class_indexes):
        self.ratings = ratings
        self.class_indexes = class_indexes
        # P, I, N for 1..l
        self.pins = []

        sigma_matrices = [SigmaMatrix([[row[i] for i in index_group]
                                       for row in self.ratings])
                          for index_group in self.class_indexes]

        for m in sigma_matrices:
            normalized = m.normalize()
            p = [[1
                  if all(n >= 0 for n in sigma)
                  and any(n > 0 for n in sigma)
                  else 0
                  for sigma in row]
                 for row in normalized]
            i = [[1
                  if all(n == 0 for n in sigma)
                  else 0
                  for sigma in row]
                 for row in normalized]
            n = [[1
                  if any(n < 0 for n in sigma)
                  and any(n > 0 for n in sigma)
                  else 0
                  for sigma in row]
                 for row in normalized]
            self.pins.append((
                BinRelation(matrix=p),
                BinRelation(matrix=i),
                BinRelation(matrix=n)))
            # for r in self.pins[-1]:
            #     r.render()
        print('-'*80)

    def solve(self):
        assert len(self.pins) > 0
        cur_p, cur_i, cur_n = self.pins[0]
        for idx, (p, i, n) in enumerate(self.pins[1:]):
            print(f"Ітерація №{idx+1}")
            next_p = ((p ^ cur_p) + (p ^ cur_i) + (p ^ cur_n)) + (i ^ cur_p)
            next_i = i ^ cur_p
            next_n = cur_n  # FIXME:
            cur_p, cur_i, cur_n = next_p, next_i, next_n
        return cur_p
