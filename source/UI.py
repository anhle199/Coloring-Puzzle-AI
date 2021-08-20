import tkinter as tk
from tkinter.constants import BOTH, BOTTOM, DISABLED, LEFT, NORMAL, RIGHT, TOP, W, X, END, Y
from tkinter.filedialog import askopenfilename
from utilities.file_io import *
from utilities.constants import CellStatus, CellSize, Algorithm, ScrollConst
from utilities.util_funcs import create_markers, calc_next_indices, cell_to_indices, get_cells, set_cells, count_cells_marked, validate
from utilities.combination_algos import generate_combination
import pysat_algo
import backtracking_algo
import brute_force_algo
import threading


def GUI():
    root = tk.Tk()
    root.title("Coloring Puzzle - AI HCMUS")

    # General Frame
    control = tk.Frame(root)
    control.pack(padx=10, side=RIGHT)
    top = tk.LabelFrame(control, text="Command")
    top.pack(padx=10, pady=10)
    creditFrame = tk.LabelFrame(control, text="Credit")
    creditFrame.pack(padx=10, pady=10, fill=X)
    bot = tk.LabelFrame(root, text="Puzzle")
    bot.pack(fill=BOTH, expand=True, padx=5, pady=10, side=LEFT)
    foot = tk.Frame(bot)
    foot.pack(fill=X, side=BOTTOM)
    right = tk.Frame(bot)
    right.pack(fill=Y, side=RIGHT)

    # variables for using
    algoMode = ["PySat", "A Star", "Brute Force", "Backtracking", "None"]
    curMode = -1
    matrix = []
    stopFlag = False
    rtFlag = False

    # Function in GUI
    def handleGetFile():  # Get file's path
        path = askopenfilename()
        if len(path) != 0:
            filePath.delete(0, END)
            filePath.insert(0, path)
        return

    def handleDisplayArray():  # Load puzzle array
        nonlocal matrix
        path = filePath.get()
        if len(path) == 0:
            warning.config(text="Please choose file or enter file path first!!!!", fg="red")
            return

        warning.config(text="Loading puzzle .....", fg="blue")
        okButton["state"] = DISABLED
        for widget in array.winfo_children():
            widget.destroy()

        try:
            matrix = read_file(path)
            size = (len(matrix), len(matrix[0]))
        except FileNotFoundError:
            warning.config(text="File does not exist!!!!", fg="red")
            okButton["state"] = NORMAL
            return
        except ValueError:
            warning.config(text="Incorrect file format!!!!", fg="red")
            okButton["state"] = NORMAL
            return

        for i in range(size[0]):
            for j in range(size[1]):
                cell = " "
                if matrix[i][j] != -1:
                    cell = str(matrix[i][j])
                box = tk.Label(
                    array,
                    text=cell,
                    width=CellSize.WIDTH,
                    height=CellSize.HEIGHT,
                    borderwidth=2,
                    relief="solid",
                    font=("Arial", CellSize.FONTSIZE),
                )
                box.grid(row=i, column=j)

        warning.config(text="Load successfully", fg="green")
        okButton["state"] = NORMAL
        return

    def handleSelectAlgo():  # Select algorithm for running
        popup = tk.Tk()
        nonlocal curMode
        mode = tk.StringVar(popup, value=str(curMode))
        popup.title("Select Algorithm")
        titleText = tk.Label(
            popup, text="Please choose one of algorithms below", font=("Arial", 10)
        )
        titleText.pack(padx=10, pady=10)
        optionWrapper = tk.LabelFrame(popup)
        optionWrapper.pack()
        values = (
            ("None", "-1"),
            ("PySat", "0"),
            ("A Star", "1"),
            ("Brute Force", "2"),
            ("Backtracking", "3")
        )

        def onClick():
            return

        def handleConfirm():
            nonlocal curMode
            curMode = int(mode.get())
            algoSelected.config(text="{}".format(algoMode[curMode]))
            popup.destroy()

        for i, item in zip(range(len(values)), values):
            tk.Radiobutton(optionWrapper, text=item[0], variable=mode, value=item[1], command=onClick,).grid(row=0, column=i)
        confirmButton = tk.Button(popup, text="Confirm", command=handleConfirm)
        confirmButton.pack(side=RIGHT, padx=10)
        popup.geometry("450x150+%d+%d" % (root.winfo_screenwidth() / 2 - 225, root.winfo_screenheight() / 2 - 75))
        return

    def renew():
        for widget in array.winfo_children():
            widget.config(bg='white', fg="black")
        return

    def redraw(markers):
        for widget, i in zip(array.winfo_children(), range(len(array.winfo_children()))):
            row = int(i / len(markers[0]))
            col = i - row * len(markers[0])
            color = "green" if markers[row][col] == CellStatus.MARKED else "red"
            widget.config(bg=color, fg="white")
        return

    def changeAllButtonState(state):
        chooseFile["state"] = state
        okButton["state"] = state
        runButton["state"] = state
        clearButton["state"] = state
        algoButton["state"] = state
        return

    ##############################################################################
    ################################# Backtracking ###############################
    ##############################################################################
    def run_backtracking_realtime():
        nonlocal stopFlag

        #############################################################################
        # Nested function
        def backtracking(markers, num_rows, num_cols, indices, i):
            if stopFlag:
                return None

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
                redraw(markers)

                status = backtracking(markers, num_rows, num_cols, indices, i + 1)
                if status != False:
                    return status

                set_cells(cells, markers, CellStatus.UNMARKED)
                redraw(markers)
            else:
                combination_list = generate_combination(cells, len(cells), k)
                for sub_list in combination_list:
                    set_cells(sub_list['extracted'], markers, CellStatus.MARKED)
                    set_cells(sub_list['remaining'], markers, CellStatus.BANNED)
                    redraw(markers)

                    status = backtracking(markers, num_rows, num_cols, indices, i + 1)
                    if status != False:
                        return status

                    set_cells(sub_list['extracted'] + sub_list['remaining'], markers, CellStatus.UNMARKED)
                    redraw(markers)

            return False
        #############################################################################


        num_rows, num_cols = len(matrix), len(matrix[0])
        markers = create_markers(matrix)
        indices = backtracking_algo.get_all_indices(matrix)
        redraw(markers)
        status = backtracking(markers, num_rows, num_cols, indices, 0)

        changeAllButtonState(NORMAL)
        if status == False:
            warning.config(text="No solution for {}".format(algoMode[curMode]), fg="green")
            return None
        elif status == None:
            warning.config(text="Stop {}".format(algoMode[curMode]), fg="red")
            return None

        model = [-num for num in range(1, num_rows * num_cols + 1)]
        for i in range(num_rows):
            for j in range(num_cols):
                if markers[i][j] == CellStatus.MARKED:
                    model[(num_rows * i) + j] = -model[(num_rows * i) + j]

        try:
            path = filePath.get().split('/')
            path[-1] = 'backtracking_output.txt'
            msg = 'Output file: ' + path[-1]
            write_file('/' + '/'.join(path), model, len(matrix), len(matrix[0]))
        except ValueError:
            msg = 'Can not write data to file!!!'

        warning.config(text="Run {} successfully\n{}".format(algoMode[curMode], msg), fg="green")
        return
    ########################################################################################



    #############################################################################
    ################################# Brute force ###############################
    #############################################################################
    def run_brute_force_realtime():
        nonlocal matrix

        #############################################################################
        # Nested function
        def brute_force(markers, num_rows, num_cols, i, j):
            if stopFlag:
                return None

            # looped through the entire matrix.
            if i == num_rows and j == num_cols:
                return validate(matrix, markers, num_rows, num_cols)

            # empty cell or cell banned.
            if matrix[i][j] == -1 or matrix[i][j] == 0:
                next_i, next_j = calc_next_indices(num_rows, num_cols, i, j)
                return brute_force(markers, num_rows, num_cols, next_i, next_j)

            cells = brute_force_algo.get_cells(matrix, markers, i, j)
            combination_list = brute_force_algo.generate_combination(cells, len(cells), matrix[i][j])
            for sub_list in combination_list:
                set_cells(sub_list, markers, CellStatus.MARKED)
                redraw(markers)

                next_i, next_j = calc_next_indices(num_rows, num_cols, i, j)
                status = brute_force(markers, num_rows, num_cols, next_i, next_j)
                if status != False:
                    return status

                set_cells(sub_list, markers, CellStatus.UNMARKED)
                redraw(markers)

            return False

        #############################################################################

        num_rows, num_cols = len(matrix), len(matrix[0])
        markers = [[CellStatus.UNMARKED for _ in range(num_cols)] for _ in range(num_rows)]
        redraw(markers)
        status = brute_force(markers, num_rows, num_cols, 0, 0)

        changeAllButtonState(NORMAL)
        if status == False:
            warning.config(text="No solution for {}".format(algoMode[curMode]), fg="green")
            return None
        elif status == None:
            warning.config(text="Stop {}".format(algoMode[curMode]), fg="red")
            return None

        model = [-num for num in range(1, num_rows * num_cols + 1)]
        for i in range(num_rows):
            for j in range(num_cols):
                if markers[i][j] == CellStatus.MARKED:
                    model[(num_rows * i) + j] = -model[(num_rows * i) + j]
        try:
            path = filePath.get().split('/')
            path[-1] = 'brute_force_output.txt'
            msg = 'Output file: ' + path[-1]
            write_file('/' + '/'.join(path), model, len(matrix), len(matrix[0]))
        except ValueError:
            msg = 'Can not write data to file!!!'

        warning.config(text="Run {} successfully\n{}".format(algoMode[curMode], msg), fg="green")
        return
    ########################################################################################



    def handleRunAlgo():  # Run algorithm to solve the puzzle
        nonlocal stopFlag
        stopFlag = False
        renew()
        if curMode == -1:
            warning.config(text="Please select an algorithm!!!", fg="red")
        else:
            if len(matrix) == 0:
                warning.config(text="Please load the puzzle first!!!", fg="red")
                return
            changeAllButtonState(DISABLED)
            warning.config(text="Running {} .....".format(algoMode[curMode]), fg="blue")

            model = None

            if curMode == Algorithm.PYSAT:
                model = pysat_algo.solve(matrix)
                changeAllButtonState(NORMAL)
            elif curMode == Algorithm.A_STAR:
                warning.config(text="{} has not been implemented yet".format(algoMode[curMode]), fg="red")
                changeAllButtonState(NORMAL)
                return
            elif curMode == Algorithm.BRUTE_FORCE:
                if (rtFlag):
                    threading.Thread(target=run_brute_force_realtime).start()
                else:
                    model = brute_force_algo.solve(matrix)
                    changeAllButtonState(NORMAL)
            elif curMode == Algorithm.BACKTRACKING:
                if (rtFlag):
                    threading.Thread(target=run_backtracking_realtime).start()
                else:
                    model = backtracking_algo.solve(matrix)
                    changeAllButtonState(NORMAL)

            if curMode == Algorithm.PYSAT or not rtFlag:
                if model == None:
                    warning.config(text="No solution with {}".format(algoMode[curMode]), fg="green")
                else:
                    try:
                        algo_names = ['pysat', 'a_star', 'brute_force', 'backtracking']
                        path = filePath.get().split('/')
                        path[-1] = algo_names[curMode] + '_output.txt'
                        msg = 'Output file: ' + path[-1]
                        write_file('/' + '/'.join(path), model, len(matrix), len(matrix[0]))
                    except ValueError:
                        msg = 'Can not write data to file!!!'

                    for widget, num in zip(array.winfo_children(), model):
                        color = "green" if num > 0 else "red"
                        widget.config(bg=color, fg="white")
                    warning.config(text="Run {} successfully\n{}".format(algoMode[curMode], msg), fg="green")

        return

    def handleClear():  # Clear puzzle
        warning.config(text="Clearing puzzle .....", fg="blue")
        nonlocal matrix
        nonlocal stopFlag
        stopFlag = True
        for widget in array.winfo_children():
            widget.destroy()
        matrix.clear()
        warning.config(text="Clear puzzle successfully", fg="green")
        return

    def handleStop():
        nonlocal stopFlag
        stopFlag = True
        return

    def handleRealtime():
        nonlocal rtFlag
        if rtFlag:
            rtFlag = False
            realtimeToggle.config(text="Realtime: OFF")
        else:
            rtFlag = True
            realtimeToggle.config(text="Realtime: ON")
        return

    # Command frame
    topLeft = tk.Frame(top, width=200, height=100)
    topLeft.pack(side=LEFT, padx=10)
    topRight = tk.Frame(top, width=200, height=100)
    topRight.pack(side=RIGHT, padx=10)

    # Command button (TOP RIGHT)
    chooseFile = tk.Button(topRight, text="Choose File", fg="black", command=handleGetFile, width=13)
    chooseFile.pack(pady=5)

    okButton = tk.Button(topRight, text="Load Puzzle", fg="black", command=handleDisplayArray, width=13)
    okButton.pack(pady=5)

    runButton = tk.Button(topRight, text="Run", command=handleRunAlgo, width=13)
    runButton.pack(pady=5)

    clearButton = tk.Button(topRight, text="Clear Puzzle", fg="black", command=handleClear, width=13)
    clearButton.pack(pady=5)

    stopButton = tk.Button(topRight, text="Stop", fg="black", command=handleStop, width=13)
    stopButton.pack(pady=5)

    realtimeToggle = tk.Button(topRight, text="Realtime: OFF", fg='black', command=handleRealtime, width=13)
    realtimeToggle.pack(pady=5)

    # Area for display data
    canvas = tk.Canvas(bot)
    canvas.pack(fill=BOTH, expand=True, side=LEFT)
    scrollY = tk.Scrollbar(right, command=canvas.yview)
    scrollY.pack(fill=Y, expand=True)
    scrollX = tk.Scrollbar(foot, orient="horizontal", command=canvas.xview)
    scrollX.pack(fill=X, expand=True)
    array = tk.Frame(canvas)

    # Bind event for scroll
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    array.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def scrollWithMouse(event):
        canvas.yview_scroll(int(-1 * (event.delta / ScrollConst.MODIFIER)), "units")

    canvas.bind_all("<MouseWheel>", scrollWithMouse)

    # Config scroll
    canvas.configure(yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)

    # Create window frame
    canvas.create_window((0, 0), window=array, anchor="nw")

    # Command Infomation (TOP LEFT)
    pathTitle = tk.Label(topLeft, text="Path:")
    filePath = tk.Entry(topLeft, width=50)
    pathTitle.pack(anchor=W)
    filePath.pack()
    algoBlock = tk.Frame(topLeft)
    algoBlock.pack(fill=X)
    algoTitle = tk.Label(algoBlock, text="Selected Algorithm:")
    algoTitle.pack(side=LEFT)
    algoSelected = tk.Label(algoBlock, text="{}".format(algoMode[curMode]), fg="blue")
    algoSelected.pack(side=LEFT)
    algoButton = tk.Button(algoBlock, text="Select Algorithm", fg="black", command=handleSelectAlgo, width=13)
    algoButton.pack(side=RIGHT, pady=10)

    # Notification while running
    mid = tk.LabelFrame(topLeft, text="Status")
    mid.pack(side=BOTTOM, fill=X)
    warning = tk.Label(mid, text="None", fg="black")
    warning.pack(padx=5, pady=5)

    # Credit
    creditText = tk.Label(creditFrame, text='Project 2: Coloring Puzzle', font=('Arial', 15))
    creditText.pack(padx=10, pady=10)
    creditTextBody1 = tk.Label(creditFrame, text='Programmed by:', font=('Arial', 10))
    creditTextBody1.pack()
    creditTextBody2 = tk.Label(creditFrame, text='Nguyen Hua Hung - 19127150\nLe Minh Huy - 19127157\nLe Hoang Anh - 19127329')
    creditTextBody2.pack(padx=10, pady=5)
    creditTextFooter = tk.Label(creditFrame, text='University Of Science - HCM City', font=('Arial', 10))
    creditTextFooter.pack(padx=10, pady=10)

    # main window size
    width = 1500 if root.winfo_screenwidth() > 1500 else root.winfo_screenwidth()
    height = 900 if root.winfo_screenheight() > 900 else root.winfo_screenheight()
    root.geometry("%dx%d+%d+%d" % (width, height, root.winfo_screenwidth() / 2 - width / 2, root.winfo_screenheight() / 2 - height / 2))
    root.update()
    root.mainloop()
