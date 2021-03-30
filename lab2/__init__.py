#!/usr/bin/env python
from common.relation import BinRelation


def parse(filename, size):
    matrices = []
    with open(filename, 'r', encoding="latin1") as f:
        lines = f.read().splitlines()
    for i in range(0, len(lines), size+1):
        l = [[int(n) for n in line.split(' ') if n.strip()]
             for line in lines[i+1:i+size+1]]
        matrices.append(l)
    return matrices


def main(args):
    print("Варіант №1")

    print("Завдання 1:")
    size = 6
    vertices = list(range(1, size+1))
    for n, matrix in enumerate(parse(args[0], size)):
        relation = BinRelation(matrix=matrix, vertices=vertices)
        print(f"Матриця №{n+1}:")
        relation.render(matrix_pairs=False)
        print(f"Симетричність: {relation.symmetric()}")
        print("Найкращі альтернативи за домінуванням:"
              f" {relation.optim_domination()}")
        print("Найкращі альтернативи за блокуванням:"
              f" {relation.optim_blocking()}")
        print()

    print('-'*80)

    print("Завдання 2:")
    size = 15
    vertices = list(range(1, size+1))
    for n, matrix in enumerate(parse(args[1], size)):
        relation = BinRelation(matrix=matrix, vertices=vertices)
        print(f"Матриця №{n+1}:")
        relation.render(matrix_pairs=False, properties=False)
        acyclic = not relation.has_cycle()
        print(f"Ациклічність: {acyclic}")
        if acyclic:
            print("Оптимізація за Нейманом-Моргерштерном:")
            print(f"C₀ = {relation.build_C0()}")
        else:
            print("К-оптимізація:")
            for k in range(1, 5):
                print(f"K = {k}")
                max, opt = relation.build_K(k)
                print(f"\tМаксимальні альтернативи: {max}")
                print(f"\tОптимальні альтернативи: {opt}")
