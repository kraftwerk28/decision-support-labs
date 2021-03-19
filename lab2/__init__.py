#!/usr/bin/env python
from common.relation import BinRelation


def parse(filename):
    matrices = []
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    for i in range(0, len(lines), 16):
        l = [[int(n) for n in line.split(' ') if n.strip()]
             for line in lines[i+1:i+16]]
        matrices.append(l)
    return matrices


def main(args):
    vertices = list(range(1, 16))
    relations = [BinRelation(matrix=m, vertices=vertices)
                 for m in parse(args[0])]
    for i, g in enumerate(relations):
        print(f"Відношення №{i+1}:")
        print(f"Ациклічне: {not g.has_cycle()}")
        if not g.has_cycle():
            print(f"Множина НМ: {g.build_C0()}")
