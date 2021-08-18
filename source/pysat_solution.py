import copy
from pysat.solvers import Glucose3
from utilities.combination_algos import generate_combination
from utilities import util_funcs


def mark_all_zero(matrix):
    markers = [[True for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                num_rows = len(matrix)
                row_start = i - 1 if i > 0 else i
                row_end = i + 1 if i < num_rows - 1 else i
                col_start = j - 1 if j > 0 else j
                col_end = j + 1 if j < len(matrix[0]) - 1 else j

                for row in range(row_start, row_end + 1):
                    for col in range(col_start, col_end + 1):
                        markers[row][col] = False
    return markers


def get_clauses(matrix, markers, i, j):
    cells = util_funcs.get_cells(matrix, markers, i, j)

    if matrix[i][j] == 0:
        return [[-item] for item in cells]

    len_cells = len(cells)
    combination_list = generate_combination(cells, len_cells, matrix[i][j])
    right_position_list = generate_combination(
        cells, len_cells, len_cells - matrix[i][j] + 1
    )

    clauses = []
    for sub_list in right_position_list:
        clauses.append(sub_list['extracted'].copy())
    for sub_list in combination_list:
        for item in sub_list['remaining']:
            clauses.append(util_funcs.negate(sub_list['extracted']))
            clauses[-1].append(-item)

    return clauses


def generate_cnf_clauses(matrix):
    markers = mark_all_zero(matrix)
    clauses = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                clauses += get_clauses(matrix, markers, i, j)

    return util_funcs.remove_duplicate_clauses(clauses)


def solve(matrix):
    clauses = generate_cnf_clauses(matrix)
    g = Glucose3()
    for clause in clauses:
        g.add_clause([number for number in clause])

    g.solve()
    model = g.get_model()
    return model


# def solve(matrix):
#     g = Glucose3()
#     matrix = [
#         [-1,  2,  3, -1, -1,  0, -1, -1, -1, -1],
#         [-1, -1, -1, -1,  3, -1,  2, -1, -1,  6],
#         [-1, -1,  5, -1,  5,  3, -1,  5,  7,  4],
#         [-1,  4, -1,  5, -1,  5, -1,  6, -1,  3],
#         [-1, -1,  4, -1,  5, -1,  6, -1, -1,  3],
#         [-1, -1, -1,  2, -1,  5, -1, -1, -1, -1],
#         [ 4, -1,  1, -1, -1, -1,  1,  1, -1, -1],
#         [ 4, -1,  1, -1, -1, -1,  1, -1,  4, -1],
#         [-1, -1, -1, -1,  6, -1, -1, -1, -1,  4],
#         [-1,  4,  4, -1, -1, -1, -1,  4, -1, -1],
#     ]
#     markers = mark_all_zero(matrix)

#     clauses = []
#     for i in range(len(matrix)):
#         for j in range(len(matrix[i])):
#             if matrix[i][j] > 0:
#                 clauses += get_clauses(matrix, markers, i, j)

#     clauses = util_funcs.remove_duplicate_clauses(clauses)
#     for clause in clauses:
#         g.add_clause([number for number in clause])

#     print('Number of clauses:', len(clauses))
#     print('Status:', g.solve())

#     model = g.get_model()
#     if model != None:
#         for i in range(0, len(model), 10):
#             for j in range(10):
#                 print('*' if model[i + j] > 0 else '_', end=' ')
#             print('')