from common.sigma_matrix import SigmaMatrix
from common.berezovsky import BerezovskyMethod


def write_solution(filename, matrix, sequence, class_indexes):
    sm = SigmaMatrix(matrix)
    vertices = list(range(1, 21))
    solutions = [
        ("Парето", sm.pareto()),
        ("Мажоритарне", sm.majoritaric()),
        ("Лексикографічне", sm.lexicographic(sequence)),
        ("Березовського", BerezovskyMethod(matrix, class_indexes).solve()),
        ("Подиновського", sm.podinovsky()),
    ]
    f = open(filename, "w")
    for idx, (name, solution) in enumerate(solutions):
        print(f"Відношення {name}:")
        solution = solution.update_vertices(vertices)
        solution.render(picture=False)
        print(f"Оптимізація за домінуванням: {solution.optim_domination()}")
        print(f"Оптимізація за блокуванням: {solution.optim_blocking()}")
        f.write(f"{idx + 1}\n{solution.raw_matrix()}")


def main(args):
    with open(args[0], "r", encoding="latin1") as f:
        lines = f.read().splitlines()
        matrix = [[int(n) for n in row.split()]
                  for row in lines[:20]]
    sequence = list([int(n[1:]) for n in lines[22].split('>')])
    # Класи впорядкованості
    class_indexes = [[int(n[1:]) for n in cl.strip('{} ').split(',')]
                     for cl in lines[-1].split('<')]
    write_solution("lab3/3-1.txt", matrix, sequence, class_indexes)
