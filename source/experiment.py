import sys
import threading
import time

import backtracking_algo
import brute_force_algo
import pysat_algo
from utilities.file_io import read_file


def experiment(type):
    matrix = read_file("input.txt")
    print("Start running...")
    start = time.time()

    result = None
    if (type == "1"):
        result = pysat_algo.solve(matrix)
    if (type == "2"):
        result = backtracking_algo.solve(matrix)
    if (type == "3"):
        result = brute_force_algo.solve(matrix)

    end = time.time()
    if result is None:
        print("No solution")
    else:
        print("The result is: ", result)

    print("Takes " + str(end - start) + " seconds to solve.")

def main():
    if (len(sys.argv) <= 1):
        print("Invalid argument.")
    else:
        th = threading.Thread(target=experiment, args=(sys.argv[1]))
        th.start()
        th.join(timeout=120)

if __name__ == '__main__':
    main()
