import sys
from typing import List
from common.relation import BinRelation
import matplotlib.pyplot as plt
from common.utils import parse456, to_fixed_str, str_row
import numpy


def get_kernel(agree_matrix, disagree_matrix, c, d):
    acc_normalized = [
        [1 if n >= c else 0 for n in row]
        for row in agree_matrix
    ]
    unacc_normalized = [
        [1 if n <= d else 0 for n in row]
        for row in disagree_matrix
    ]
    vertices = range(1, len(agree_matrix)+1)
    acc_matrix = BinRelation(matrix=acc_normalized, vertices=vertices)
    unacc_matrix = BinRelation(matrix=unacc_normalized, vertices=vertices)
    relation = (acc_matrix ^ unacc_matrix).update_vertices(vertices)
    return relation.build_C0()

def part2(agree_matrix, disagree_matrix):
    d_space = numpy.linspace(0, 0.5, 99, endpoint=False)[1:]
    c_space = numpy.linspace(0.5, 1, 100)
    _, plots = plt.subplots(ncols=3)

    c = .5
    y_values = []
    for d in d_space:
        kernel = get_kernel(agree_matrix, disagree_matrix, c, d)
        y_values.append(len(kernel))
    # plt.subplot(1, 1, 1)
    plots[0].set_title("c = 0.5, 0 < d < 0.5")
    plots[0].plot(numpy.linspace(0.1, 0.49, 98), y_values)

    d = 0.49
    y_values = []
    for c in c_space:
        kernel = get_kernel(agree_matrix, disagree_matrix, c, d)
        y_values.append(len(kernel))
    plots[1].set_title("0.5 ≤ c ≤ 1, d = 0.49")
    plots[1].plot(numpy.linspace(0, 0.5, 100), y_values)

    y_values = []
    for c, d in zip(c_space, d_space):
        kernel = get_kernel(agree_matrix, disagree_matrix, c, d)
        y_values.append(len(kernel))
    plots[2].set_title("0.5 ≤ c ≤ 1, 0 < d < 0.5")
    plots[2].plot(numpy.linspace(0.1, 0.49, 98), y_values)

    plt.show()


def main(args):
    matrix, k, c, d = parse456(args[0])

    k_sum = sum(k)
    weights = [n / k_sum for n in k]

    outfile = open("lab4/Var-1-Амброс.txt", 'w')
    # outfile = sys.stdout
    out = lambda *args: print(*args, file=outfile)

    agree_matrix: List[List[float]] = []
    for row in matrix:
        r = []
        for row2 in matrix:
            if row == row2:
                r.append(0)
                continue
            s = 0
            for i, (a, b) in enumerate(zip(row, row2)):
                if a >= b:
                    s += weights[i]
            r.append(s)
        agree_matrix.append(r)

    disagree_matrix: List[List[float]] = []
    for row in matrix:
        r = []
        for row2 in matrix:
            if row == row2:
                r.append(1)
                continue
            numerators, denominators = [], []
            for i, (a, b) in enumerate(zip(row, row2)):
                if a >= b:
                    continue
                column = [row[i] for row in matrix]
                numerators.append(weights[i] * abs(a-b))
                denominators.append(weights[i] * abs(min(column) - max(column)))
            if not denominators:
                r.append(0.)
            else:
                r.append(max(numerators) / max(denominators))
        disagree_matrix.append(r)

    acc_normalized = [[1 if n >= c else 0 for n in row] for row in agree_matrix]
    for row in acc_normalized:
        print(' '.join(str(n) for n in row))
    unacc_normalized = [
        [1 if n <= d else 0 for n in row]
        for row in disagree_matrix
    ]
    print()
    for row in unacc_normalized:
        print(' '.join(str(n) for n in row))
    vertices = range(1, len(matrix)+1)
    acc_matrix = BinRelation(matrix=acc_normalized, vertices=vertices)
    unacc_matrix = BinRelation(matrix=unacc_normalized, vertices=vertices)
    relation = (acc_matrix ^ unacc_matrix).update_vertices(vertices)

    out("матриця індексів узгодження C")
    for row in agree_matrix:
        out(' '.join(to_fixed_str(n) for n in row))
    out("матриця індексів неузгодження D")
    for row in disagree_matrix:
        out(' '.join(to_fixed_str(n) for n in row))
    out("Значення порогів для індексів узгодження та неузгодження c, d")
    out(f"{to_fixed_str(c)} {to_fixed_str(d)}")
    out("Відношення для порогових значень c, d:")
    for row in relation.matrix:
        out(' ' + '  '.join(str(n) for n in row) + ' ')
    out("Ядро відношення:")
    out(' '.join(str(n) for n in relation.build_C0()))

    part2(agree_matrix, disagree_matrix)
