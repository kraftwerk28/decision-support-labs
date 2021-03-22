from sigma_matrix import SigmaMatrix

if __name__ == "__main__":
    m = [[2, 1, 8, 9],
         [10, 4, 9, 9],
         [8, 1, 6, 7],
         [10, 4, 2, 5],
         [9, 6, 10, 2]]
    sm = SigmaMatrix(m)
    sm.pareto().render()
    sm.majoritaric().render()
    sm.lexicographic().render()
    print(sm.lexicographic().optim_domination())
