import platform

class CellStatus:
    BANNED = None
    MARKED = True
    UNMARKED = False

class CellSize:
    WIDTH = 9
    HEIGHT = 4
    FONTSIZE = 12
    if platform.system() == 'Darwin':
        WIDTH = 5
        HEIGHT = 2
        FONTSIZE = 20

class Algorithm:
    NONE = -1
    PYSAT = 0
    A_STAR = 1
    BRUTE_FORCE = 2
    BACKTRACKING = 3

class ScrollConst:
    MODIFIER = 120
    if platform.system() == 'Darwin':
        MODIFIER = 1
