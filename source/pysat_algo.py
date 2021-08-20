from pysat.solvers import Glucose3
from utilities.combination_algos import generate_combination
from utilities.util_funcs import calc_no, get_cells, negate, create_markers, remove_duplicate_clauses


def get_clauses_for_zero(matrix, markers, i, j):
    num_rows = len(matrix)
    row_start = i - 1 if i > 0 else i
    row_end = i + 1 if i < num_rows - 1 else i
    col_start = j - 1 if j > 0 else j
    col_end = j + 1 if j < len(matrix[0]) - 1 else j

    clauses = []
    for row in range(row_start, row_end + 1):
        for col in range(col_start, col_end + 1):
            cell = calc_no(row, col, num_rows)
            clauses.append([-cell])

    return clauses


def get_clauses(matrix, markers, i, j):
    cells, num_cells_marked = get_cells(matrix, markers, i, j)
    len_cells = len(cells)
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
            elif matrix[i][j] == 0:
                clauses += get_clauses_for_zero(matrix, markers, i, j)

    return remove_duplicate_clauses(clauses)


def solve(matrix):
    clauses = generate_cnf_clauses(matrix)
    g = Glucose3()
    for clause in clauses:
        g.add_clause([number for number in clause])

    status = g.solve()
    return g.get_model() if status else None
