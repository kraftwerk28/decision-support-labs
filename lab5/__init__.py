import sys
from common.utils import parse456, transpose, to_fixed_str, str_row

def main(args):
    matrix, k, _, _ = parse456(args[0])
    weights = [x/sum(k) for x in k]
    outfile = sys.stdout
    out = lambda *args: print(*args, file=outfile)

    if '--test' in args:
        matrix = [
            [5, 8, 4],
            [7, 6, 8],
            [8, 8, 6],
            [7, 4, 6],
        ]
        weights = [.3, .4, .3]

    out("Метод TOPSIS:")
    for row in matrix:
        out(str_row(row))
    out(str_row(weights))

    denoms = [sum(x**2 for x in row)**.5 for row in transpose(matrix)]
    normalized = [
        [x / denoms[i] for i, x in enumerate(row)]
        for row in matrix
    ]

    out("Нормалізовані оцінки:")
    for row in normalized:
        out(str_row(row))
    normalized_weighted = [
        [x * weights[i] for i, x in enumerate(row)]
        for row in normalized
    ]

    out("Зважені нормалізовані оцінки:")
    for row in normalized_weighted:
        out(str_row(row))
    pis = [max(row) for row in transpose(normalized_weighted)]
    nis = [min(row) for row in transpose(normalized_weighted)]
    out("\nА)")
    out("Вектор PIS: (" + str_row(pis) + ")")
    out("Вектор NIS: (" + str_row(nis) + ")")

    pis_distance = [
        sum((a-b)**2 for a, b in zip(row, pis)) ** 0.5
        for row in normalized_weighted
    ]
    nis_distance = [
        sum((a-b)**2 for a, b in zip(row, nis)) ** 0.5
        for row in normalized_weighted
    ]

    out("C*:")
    c_star = [nis / (pis + nis) for pis, nis in zip(pis_distance, nis_distance)]
    out(str_row(c_star))
    best = max(zip(range(1, len(matrix)+1), c_star), key=lambda x: x[1])[0]
    out(f"Найкраща альтернатива: {best}")

    # k1-k7 -> max; k8-k12 -> min
    pis = [
        max(row) if i < 7 else min(row)
        for i, row in enumerate(normalized_weighted)
    ]
    nis = [
        min(row) if i < 7 else max(row)
        for i, row in enumerate(normalized_weighted)
    ]
    out("\nБ)")
    out("Вектор PIS: (" + str_row(pis) + ")")
    out("Вектор NIS: (" + str_row(nis) + ")")

    pis_distance = [
        sum((a-b)**2 for a, b in zip(row, pis)) ** 0.5
        for row in normalized_weighted
    ]
    nis_distance = [
        sum((a-b)**2 for a, b in zip(row, nis)) ** 0.5
        for row in normalized_weighted
    ]

    out("C*:")
    c_star = [nis / (pis + nis) for pis, nis in zip(pis_distance, nis_distance)]
    out(str_row(c_star))
    best = max(zip(range(1, len(matrix)+1), c_star), key=lambda x: x[1])[0]
    out(f"Найкраща альтернатива: {best}\n")

    out("Метод VIKOR:")
    maximums = [max(row) for row in transpose(matrix)]
    deltas = [max(row) - min(row) for row in transpose(matrix)]

    normalized = [
        [(maximums[i] - n) / (deltas[i]) for n in row]
        for i, row in enumerate(transpose(matrix))
    ]
    out("Нормалізовані інтервали:")
    for row in transpose(normalized):
        out(str_row(row))
    normalized_weights = [
        [n*weights[i] for n in row]
        for i, row in enumerate(normalized)
    ]

    out("Нормалізовані зважені інтервали:")
    for row in transpose(normalized_weights):
        out(str_row(row))

    sj, rj, qj = [], [], []
    for row in transpose(normalized_weights):
        sj.append(sum(row))
        rj.append(max(row))
    for s, j in zip(sj, rj):
        s_delta = max(sj)-min(sj)
        j_delta = max(rj)-min(rj)
        qj.append(.5 * ((s-min(sj)) / s_delta) + .5 * ((j-min(rj)) / j_delta))

    out(' '.join(s.ljust(5) for s in ("Sj:", "Rj:", "Qj:")))
    for sjq in zip(sj, rj, qj):
        out(str_row(sjq))

    ranging = sorted(zip(range(1, len(matrix)+1), qj), key=lambda x: x[1])
    out(' < '.join('A'+str(v) for v, _ in ranging))
