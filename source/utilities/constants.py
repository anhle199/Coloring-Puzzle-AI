import platform

cell_width = 9
cell_height = 4
if platform.system() == 'Darwin':
    cell_width = 5
    cell_height = 2