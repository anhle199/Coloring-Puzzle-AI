def read_file(file_path):
    try:
        reader = open(file_path, 'r')

        # read and assign size of matrix (board)
        size = reader.readline().rstrip('\n').split()
        num_rows = int(size[0])
        num_cols = int(size[1])

        # read and assign data in matrix (board)
        board = [reader.readline().rstrip('\n').split() for _ in range(num_rows)]
        matrix = [[int(cell) for cell in row] for row in board]
        reader.close()
    except FileNotFoundError:
        raise ValueError('File does not exist!!!')
    except ValueError:
        raise ValueError('Matrix contains data that is not a number!!!')

    return matrix


def write_file(file_path, matrix):
    try:
        writer = open(file_path, 'w')

        num_rows = len(matrix)
        num_cols = len(matrix[0])
        writer.write(str(num_rows) + ' ' + str(num_cols))
        writer.writelines(['\n' + ' '.join(row) for row in matrix])
        writer.close()
    except:
        raise ValueError('Can not write data to file!!!')
