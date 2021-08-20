from utilities.combination_algos import generate_combination
from utilities.util_funcs import get_cells, set_cells, create_markers, calc_no
from utilities.constants import CellStatus
from brute_force import count_cells_marked


def get_all_indices(matrix):
    indices = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] > 0:
                indices.append((i, j))
    return indices


def backtracking(matrix, markers, num_rows, num_cols, indices, i):
    # looped through the entire matrix.
    if i == len(indices):
        return True

    row, col = indices[i]
    if count_cells_marked(markers, row, col) > matrix[row][col]:
        return False

    cells, num_cells_marked = get_cells(matrix, markers, row, col)
    k = matrix[row][col] - num_cells_marked  # number of remaining cells that can color adjacent matrix[i][j] cell.
    if k == 0:
        set_cells(cells, markers, CellStatus.BANNED)

        status = backtracking(matrix, markers, num_rows, num_cols, indices, i + 1)
        if status:
            return status

        set_cells(cells, markers, CellStatus.UNMARKED)
    else:
        combination_list = generate_combination(cells, len(cells), k)
        for sub_list in combination_list:
            set_cells(sub_list['extracted'], markers, CellStatus.MARKED)
            set_cells(sub_list['remaining'], markers, CellStatus.BANNED)

            status = backtracking(matrix, markers, num_rows, num_cols, indices, i + 1)
            if status:
                return status

            set_cells(sub_list['extracted'] + sub_list['remaining'], markers, CellStatus.UNMARKED)

    return False

def count_cells_marked(markers, i, j):
    num_rows = len(markers)
    row_start = i - 1 if i > 0 else i
    row_end = i + 1 if i < num_rows - 1 else i
    col_start = j - 1 if j > 0 else j
    col_end = j + 1 if j < len(markers[0]) - 1 else j

    count = 0
    for row in range(row_start, row_end + 1):
        for col in range(col_start, col_end + 1):
            if markers[row][col] == CellStatus.MARKED:
                count += 1

    return count


def solve(matrix):
    num_rows, num_cols = len(matrix), len(matrix[0])
    markers = create_markers(matrix)
    indices = get_all_indices(matrix)
    status = backtracking(matrix, markers, num_rows, num_cols, indices, 0)
    if not status:
        return None

    model = [-num for num in range(1, num_rows * num_cols + 1)]
    for i in range(num_rows):
        for j in range(num_cols):
            if markers[i][j] == CellStatus.MARKED:
                model[(num_rows * i) + j] = -model[(num_rows * i) + j]

    return model
