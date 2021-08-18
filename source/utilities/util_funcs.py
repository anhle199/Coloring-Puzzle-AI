# def validate_matrix(matrix):


def negate(numbers):
    return [-num for num in numbers]


def calc_no(i, j, num_rows):
    return (num_rows * i) + j + 1


def get_cells(matrix, markers, i, j):
    num_rows = len(matrix)
    row_start = i - 1 if i > 0 else i
    row_end = i + 1 if i < num_rows - 1 else i
    col_start = j - 1 if j > 0 else j
    col_end = j + 1 if j < len(matrix[0]) - 1 else j

    cells = []
    for row in range(row_start, row_end + 1):
        for col in range(col_start, col_end + 1):
            if markers[row][col]:
                cell = calc_no(row, col, num_rows)
                cells.append(cell)

    return cells


def remove_duplicate_clauses(clauses):
    clauses_sorted = [list(set(clause)) for clause in clauses]
    clauses_distinct = list(set([''.join(str(clause)) for clause in clauses_sorted]))
    return [list(map(int, clause.lstrip('[').rstrip(']').split(', '))) for clause in clauses_distinct]
