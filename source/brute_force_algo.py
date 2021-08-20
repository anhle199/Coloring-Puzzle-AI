from utilities.util_funcs import create_markers, calc_next_indices, set_cells, calc_no, count_cells_marked, validate
from utilities.constants import CellStatus


def get_combination(numbers, markers):
    result = []
    for (item, status) in zip(numbers, markers):
        if status:
            result.append(item)

    return result


def generate_combination_implement(numbers, markers, n, k, pos, result):
    if k == 0:
        return
    for i in range(pos, n):
        if not markers[i]:
            markers[i] = True
            if k - 1 == 0:
                result.append(get_combination(numbers, markers))
            else:
                generate_combination_implement(numbers, markers, n, k - 1, i + 1, result)
            markers[i] = False


def generate_combination(numbers, n, k):
    markers = [False for _ in range(n)]
    result = []
    generate_combination_implement(numbers, markers, n, k, 0, result)
    return result


def get_cells(matrix, markers, i, j):
    num_rows = len(matrix)
    row_start = i - 1 if i > 0 else i
    row_end = i + 1 if i < num_rows - 1 else i
    col_start = j - 1 if j > 0 else j
    col_end = j + 1 if j < len(matrix[0]) - 1 else j

    cells = []
    for row in range(row_start, row_end + 1):
        for col in range(col_start, col_end + 1):
            cell = calc_no(row, col, num_rows)
            cells.append(cell)

    return cells


# True: solved
# False: no solution
def brute_force(matrix, markers, num_rows, num_cols, i, j):
    # looped through the entire matrix.
    if i == num_rows and j == num_cols:
        return validate(matrix, markers, num_rows, num_cols)

    # empty cell or cell banned.
    if matrix[i][j] == -1 or matrix[i][j] == 0:
        next_i, next_j = calc_next_indices(num_rows, num_cols, i, j)
        return brute_force(matrix, markers, num_rows, num_cols, next_i, next_j)

    cells = get_cells(matrix, markers, i, j)
    combination_list = generate_combination(cells, len(cells), matrix[i][j])
    for sub_list in combination_list:
        set_cells(sub_list, markers, CellStatus.MARKED)

        next_i, next_j = calc_next_indices(num_rows, num_cols, i, j)
        status = brute_force(matrix, markers, num_rows, num_cols, next_i, next_j)
        if status:
            return status

        set_cells(sub_list, markers, CellStatus.UNMARKED)

    return False


def solve(matrix):
    num_rows, num_cols = len(matrix), len(matrix[0])
    markers = [[CellStatus.UNMARKED for _ in range(num_cols)] for _ in range(num_rows)]
    status = brute_force(matrix, markers, num_rows, num_cols, 0, 0)
    if not status:
        return None

    model = [-num for num in range(1, num_rows * num_cols + 1)]
    for i in range(num_rows):
        for j in range(num_cols):
            if markers[i][j] == CellStatus.MARKED:
                model[(num_rows * i) + j] = -model[(num_rows * i) + j]

    return model