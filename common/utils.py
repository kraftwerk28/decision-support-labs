from decimal import Decimal

def parse456(filename: str):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    matrix = [[int(n) for n in line.split()] for line in lines[1:16]]
    k = [int(n) for n in lines[17].split()]
    c, d = [float(n) for n in lines[19].split()]
    return matrix, k, c, d

def to_fixed_str(n: float, points: int = 3) -> str:
    dec = Decimal(n).quantize(Decimal('.' + '0'*points))
    return str(dec)

def transpose(matrix):
    assert len(matrix) > 0
    assert all(len(row) == len(matrix[0]) for row in matrix)
    return [
        [matrix[i][j] for i in range(len(matrix))]
        for j in range(len(matrix[0]))
    ]

def str_row(row, spaces=1):
    return (spaces*' ').join(to_fixed_str(n) for n in row)
