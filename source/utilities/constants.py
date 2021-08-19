import platform

class CellStatus:
    BANNED = None
    MARKED = True
    UNMARKED = False

class CellSize:
    WIDTH = 9
    HEIGHT = 4
    if platform.system() == 'Darwin':
        WIDTH = 5
        HEIGHT = 2

class Algorithm:
    PYSAT = 0
    A_STAR = 1
    BRUTE_FORCE = 2
    BACKTRACKING = 3
