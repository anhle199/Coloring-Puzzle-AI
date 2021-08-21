# Coloring Puzzle

## Usage

- Please install `Python` first.
- Then, install [pysat] library:
    - Open terminal (MacOS) or cmd (Windows).
    - Run one in three commands below to install `pysat`.
        ```
        pip install python-sat
        ```
        ```
        pip install python-sat[pblib,aiger]
        ```
        ```
        pip install pysat
        ```
    - Run the program:
        - Direct the current path to [source] folder in terminal.
        - Run one in two commands below.
            ```
            python main.py
            ```
            ```
            python3 main.py
            ```

## Contributors

| Student ID | Full name |
| :--------: | --------------- |
| 19127150   | Nguyen Hua Hung |
| 19127157   | Le Minh Huy     |
| 19127329   | Le Hoang Anh    |

## Experiment result

-   The experiment is done using a console.
-   The result is represented in the table below.
-   Because of doing experiments on the console, our team has to change the code in [main.py].
-   After the testing process, we change the code to the origin that is the submission version in the source folder.
-   Because some cases take a lot of time to solve, the time limit is 2 minutes to avoid memory overloading and time consuming.
-   In this experiment, three algorithms are used except A\* because of incomplete implementation.
-   All test cases are stored in file [test_cases.txt] with different sizes.

|  Algorithms  |         |         |         |         |         |         |
| :----------: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: |
|              |   3x3   |   5x5   |   7x7   |   9x9   |  11x11  |  20x20  |
|    Pysat     | 0.00598 | 0.01795 | 0.09175 | 0.10362 | 0.29026 | 0.65518 |
| Backtracking | 0.00102 | 0.00199 | 0.00096 | 0.00099 | 0.00295 | 0.23636 |
| Brute-force  | 0.01598 | timeout | timeout | timeout | timeout | timeout |


[pysat]: https://pysathq.github.io/installation.html
[source]: ./source
[main.py]: ./source/main.py
[test_cases.txt]: ./source/test_cases.txt