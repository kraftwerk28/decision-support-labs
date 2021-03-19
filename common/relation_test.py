from relation import BinRelation


if __name__ == "__main__":
    m2 = [[0, 1, 0, 1, 1, 1],
          [0, 0, 0, 0, 1, 0],
          [1, 1, 0, 1, 1, 1],
          [0, 1, 0, 0, 1, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 1, 0, 1, 1, 0]]
    m3 = [[1, 1, 0, 1, 1, 1],
          [0, 1, 0, 0, 1, 0],
          [1, 1, 1, 1, 1, 1],
          [0, 1, 0, 1, 1, 0],
          [0, 0, 0, 0, 1, 0],
          [0, 1, 0, 1, 1, 1]]
    m4 = [[0, 1, 1, 0, 0, 0],
          [0, 0, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 1, 0, 1, 1],
          [0, 0, 1, 0, 0, 0],
          [0, 0, 1, 0, 1, 0]]
    m5 = [[1 if i == j else c for j, c in enumerate(row)]
          for i, row in enumerate(m4)]
    r6 = BinRelation.from_assos_tuples(2, [1, 3, 6],
                                       5, [1, 3, 6],
                                       1, [3, 6],
                                       3, [6],
                                       4, [6])
    r8 = BinRelation.from_assos_tuples(2, [2, 1, 3, 6],
                                       5, [5, 1, 3, 6],
                                       1, [1, 3, 6],
                                       3, [3, 6],
                                       4, [4, 6],
                                       6, [6])
    # r6.render()
    # print(r6.x_star_p())
    # print(r6.x_zero_p())
    r9 = BinRelation(matrix=[[1, 0, 1, 0, 1],
                             [1, 1, 1, 0, 1],
                             [1, 0, 1, 0, 1],
                             [1, 0, 1, 0, 1],
                             [1, 0, 1, 0, 1]])
    r8 = BinRelation(matrix=[[1, 0, 1, 0, 1],
                             [1, 1, 1, 1, 1],
                             [1, 0, 1, 0, 1],
                             [1, 1, 1, 1, 1],
                             [1, 0, 1, 0, 0]],
                     vertices=[1, 2, 3, 4, 5])

    m6 = [[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
          [0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    rel = BinRelation(matrix=m6, vertices=list(range(1, 11)))
    rel.render()
    NM_solution = rel.build_C0()
    print(NM_solution)
    print(rel.optimal_by_NM(NM_solution))
    # relation = r8
    # relation.render()
    # print(relation.x_star_r())
    # print(relation.x_star_star_r())
