from utilities.util_funcs import model_to_markers

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


def write_file(file_path, model, num_rows, num_cols):
    try:
        writer = open(file_path, 'w')
        writer.write(str(num_rows) + ' ' + str(num_cols))
        writer.writelines(['\n' + ' '.join(row) for row in model_to_markers(model, num_rows, num_cols)])
        writer.close()
    except:
        raise ValueError('Can not write data to file!!!')
