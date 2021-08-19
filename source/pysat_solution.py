import copy
from pysat.solvers import Glucose3
from utilities.combination_algos import generate_combination
from utilities.util_funcs import get_cells, negate, create_markers, remove_duplicate_clauses


def get_clauses(matrix, markers, i, j):
    cells, len_cells = get_cells(matrix, markers, i, j)

    if matrix[i][j] == 0:
        return [[-item] for item in cells]

    combination_list = generate_combination(cells, len_cells, matrix[i][j])
    right_position_list = generate_combination(cells, len_cells, len_cells - matrix[i][j] + 1)

    clauses = []
    for sub_list in right_position_list:
        clauses.append(sub_list['extracted'].copy())
    for sub_list in combination_list:
        for item in sub_list['remaining']:
            clauses.append(negate(sub_list['extracted']))
            clauses[-1].append(-item)

    return clauses


def generate_cnf_clauses(matrix):
    markers = create_markers(matrix)
    clauses = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                clauses += get_clauses(matrix, markers, i, j)

    return remove_duplicate_clauses(clauses)


def solve(matrix):
    clauses = generate_cnf_clauses(matrix)
    g = Glucose3()
    for clause in clauses:
        g.add_clause([number for number in clause])

    status = g.solve()
    return g.get_model() if status else None
