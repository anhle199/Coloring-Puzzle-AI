from utilities.combination_algos import generate_combination
from utilities.util_funcs import calc_next_indices, get_cells, set_cells, create_markers, calc_no
from utilities.constants import CellStatus


def backtracking(matrix, markers, num_rows, num_cols, i, j):
    # looped through the entire matrix.
    if i == num_rows and j == num_cols:
        return True

    # empty cell or cell banned.
    if matrix[i][j] == -1 or matrix[i][j] == 0:
        next_i, next_j = calc_next_indices(num_rows, num_cols, i, j)
        return backtracking(matrix, markers, num_rows, num_cols, next_i, next_j)

    cells, max_cells = get_cells(matrix, markers, i, j)
    k = matrix[i][j] - (max_cells - len(cells))  # number of remaining cells that can color adjacent matrix[i][j] cell.
    if k == 0:
        set_cells(cells, markers, CellStatus.BANNED)#

        next_i, next_j = calc_next_indices(num_rows, num_cols, i, j)
        status = backtracking(matrix, markers, num_rows, num_cols, next_i, next_j)
        if status:
            return status

        set_cells(cells, markers, CellStatus.UNMARKED)#
    else:
        combination_list = generate_combination(cells, len(cells), k)
        for sub_list in combination_list:
            set_cells(sub_list['extracted'], markers, CellStatus.MARKED)#
            set_cells(sub_list['remaining'], markers, CellStatus.BANNED)#

            next_i, next_j = calc_next_indices(num_rows, num_cols, i, j)
            status = backtracking(matrix, markers, num_rows, num_cols, next_i, next_j)
            if status:
                return status

            set_cells(sub_list['extracted'] + sub_list['remaining'], markers, CellStatus.UNMARKED)#

    return False


def solve(matrix):
    num_rows, num_cols = len(matrix), len(matrix[0])
    markers = create_markers(matrix)
    status = backtracking(matrix, markers, num_rows, num_cols, 0, 0)
    if not status:
        return None

    model = [-num for num in range(1, num_rows * num_cols + 1)]
    for i in range(num_rows):
        for j in range(num_cols):
            if markers[i][j] == CellStatus.MARKED:
                model[(num_rows * i) + j] = -model[(num_rows * i) + j]

    return model
