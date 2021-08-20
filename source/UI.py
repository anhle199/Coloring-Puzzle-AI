import tkinter as tk
from tkinter.constants import BOTH, BOTTOM, DISABLED, LEFT, NORMAL, RIGHT, TOP, W, X, END, Y
from tkinter.filedialog import askopenfilename
from utilities.file_io import *
from utilities.constants import CellStatus, CellSize, Algorithm, ScrollConst
from utilities.util_funcs import create_markers, calc_next_indices, cell_to_indices, get_cells
from utilities.combination_algos import generate_combination
import pysat_solution
from backtracking import backtracking, count_cells_marked, solve
import brute_force
import threading


def GUI():
    root = tk.Tk()
    root.title('Coloring Puzzle - AI HCMUS')

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
    algoMode = ['PySat', 'A Star', 'BruteForce', 'Backtracking', 'None']
    curMode = -1
    matrix = []
    stopFlag = False
    rtFlag = False

    # Function in GUI
    def handleGetFile(): # Get file's path
        path = askopenfilename()
        if (len(path) != 0):
            filePath.delete(0, END)
            filePath.insert(0, path)
        return

    # def handleCredit(): # Show credit information
    #     popup = tk.Tk()
    #     popup.title('Credit')
    #     creditText = tk.Label(popup, text='Project 2: Coloring Puzzle', font=('Arial', 15))
    #     creditText.pack(padx=10, pady=10)
    #     creditTextBody1 = tk.Label(popup, text='Programmed by:', font=('Arial', 10))
    #     creditTextBody1.pack()
    #     creditTextBody2 = tk.Label(popup, text='Nguyen Hua Hung - 19127150\nLe Minh Huy - 19127157\nLe Hoang Anh - 19127329')
    #     creditTextBody2.pack(padx=10, pady=5)
    #     creditTextFooter = tk.Label(popup, text='University Of Science - HCM City', font=('Arial', 10))
    #     creditTextFooter.pack(padx=10, pady=10)
    #     popup.geometry('300x200+%d+%d' % (root.winfo_screenwidth() / 2 - 150, root.winfo_screenheight() / 2 - 100))
    #     return

    def handleDisplayArray(): # Load puzzle array
        nonlocal matrix
        path = filePath.get()
        if (len(path) == 0):
            warning.config(text='Please choose file or enter file path first!!!!', fg='red')
            return

        warning.config(text='Loading puzzle .....', fg='blue')
        okButton['state'] = DISABLED
        for widget in array.winfo_children():
            widget.destroy()

        try:
            matrix = read_file(path)
            size = (len(matrix), len(matrix[0]))
        except FileNotFoundError:
            warning.config(text='File does not exist!!!!', fg='red')
            okButton['state'] = NORMAL
            return
        except ValueError:
            warning.config(text='Incorrect file format!!!!', fg='red')
            okButton['state'] = NORMAL
            return

        for i in range(size[0]):
            for j in range(size[1]):
                cell = ' '
                if matrix[i][j] != -1:
                    cell = str(matrix[i][j])
                box = tk.Label(array, text=cell, width=CellSize.WIDTH, height=CellSize.HEIGHT, borderwidth=2, relief='solid', font=('Arial', CellSize.FONTSIZE))
                box.grid(row=i, column=j)

        warning.config(text='Load successfully', fg='green')
        okButton['state'] = NORMAL
        return

    def handleSelectAlgo(): # Select algorithm for running
        popup = tk.Tk()
        nonlocal curMode
        mode = tk.StringVar(popup, value=str(curMode))
        popup.title('Select Algorithm')
        titleText = tk.Label(popup, text='Please choose one of algorithms below', font=('Arial', 10))
        titleText.pack(padx=10, pady=10)
        optionWrapper = tk.LabelFrame(popup)
        optionWrapper.pack()
        values = (
            ('None', '-1'),
            ('PySat', '0'),
            ('A Star', '1'),
            ('BruteForce', '2'),
            ('Backtracking', '3')
            # ('None', Algorithm.PYSAT),
            # ('PySat', Algorithm.PYSAT),
            # ('A Star', Algorithm.A_STAR),
            # ('BruteForce', Algorithm.BRUTE_FORCE),
            # ('Backtracking', Algorithm.BACKTRACKING)
        )
        def onClick():
            return
        def handleConfirm():
            nonlocal curMode
            curMode = int(mode.get())
            algoSelected.config(text='{}'.format(algoMode[curMode]))
            popup.destroy()
        for i, item in zip(range(len(values)), values):
            tk.Radiobutton(optionWrapper, text=item[0], variable=mode, value=item[1], command=onClick).grid(row=0, column=i)
        confirmButton = tk.Button(popup, text='Confirm', command=handleConfirm)
        confirmButton.pack(side=RIGHT, padx=10)
        popup.geometry('450x150+%d+%d' % (root.winfo_screenwidth() / 2 - 225, root.winfo_screenheight() / 2 - 75))
        return
    
    def redraw(markers):
        for widget, i in zip(array.winfo_children(), range(len(array.winfo_children()))):
            row = int(i / len(markers[0]))
            col = i - row * len(markers[0])
            color = 'green' if markers[row][col] == CellStatus.MARKED else 'red'
            widget.config(bg=color, fg='white')
        return

    def changeAllButtonState(state):
        chooseFile['state'] = state
        okButton['state'] = state
        runButton['state'] = state
        clearButton['state'] = state
        algoButton['state'] = state
        return

    ########################################################################
    def set_cells(cells, markers, val):
        num_rows, num_cols = len(markers), len(markers[0])
        for num in cells:
            row, col = cell_to_indices(num, num_rows, num_cols)
            markers[row][col] = val

    def run_backtracking():
        nonlocal stopFlag
        def create_markers(matrix):
            markers = [[CellStatus.UNMARKED for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    if matrix[i][j] == 0:
                        num_rows = len(matrix)
                        row_start = i - 1 if i > 0 else i
                        row_end = i + 1 if i < num_rows - 1 else i
                        col_start = j - 1 if j > 0 else j
                        col_end = j + 1 if j < len(matrix[0]) - 1 else j

                        for row in range(row_start, row_end + 1):
                            for col in range(col_start, col_end + 1):
                                markers[row][col] = CellStatus.BANNED
            return markers

        def backtracking(matrix, markers, num_rows, num_cols, i, j):
            if (stopFlag):
                return None
            # looped through the entire matrix.
            if i == num_rows and j == num_cols:
                return True

            # empty cell or cell banned.
            if matrix[i][j] == -1 or matrix[i][j] == 0:
                next_i, next_j = calc_next_indices(num_rows, num_cols, i, j)
                return backtracking(matrix, markers, num_rows, num_cols, next_i, next_j)

            if count_cells_marked(markers, i, j) > matrix[i][j]:
                return False

            cells, max_cells = get_cells(matrix, markers, i, j)
            k = matrix[i][j] - (max_cells - len(cells))  # number of remaining cells that can color adjacent matrix[i][j] cell.
            if k == 0:
                set_cells(cells, markers, CellStatus.BANNED)#
                redraw(markers) #markers BANNED = UNMARKED = đỏ, MARKED = xanh

                next_i, next_j = calc_next_indices(num_rows, num_cols, i, j)
                status = backtracking(matrix, markers, num_rows, num_cols, next_i, next_j)
                if status != False:
                    return status

                set_cells(cells, markers, CellStatus.UNMARKED)#
                redraw(markers)
            else:
                combination_list = generate_combination(cells, len(cells), k)
                for sub_list in combination_list:
                    set_cells(sub_list['extracted'], markers, CellStatus.MARKED)#
                    #redraw(markers)
                    set_cells(sub_list['remaining'], markers, CellStatus.BANNED)#
                    redraw(markers)

                    next_i, next_j = calc_next_indices(num_rows, num_cols, i, j)
                    status = backtracking(matrix, markers, num_rows, num_cols, next_i, next_j)
                    if status != False:
                        return status

                    set_cells(sub_list['extracted'] + sub_list['remaining'], markers, CellStatus.UNMARKED)#
                    redraw(markers)

            return False
        
        num_rows, num_cols = len(matrix), len(matrix[0])
        markers = create_markers(matrix) #
        #threading.Thread(target=redraw, args=(markers)).start()
        redraw(markers)
        status = backtracking(matrix, markers, num_rows, num_cols, 0, 0)
        changeAllButtonState(NORMAL)
        if status == False:
            warning.config(text='No solution for {}'.format(algoMode[curMode]), fg='green')
            return None
        elif status == None:
            warning.config(text='Stop {}'.format(algoMode[curMode]), fg='red')
            return None
        #threading.Thread(target=redraw, args=(markers)).start()
        redraw(markers)

        # model = [-num for num in range(1, num_rows * num_cols + 1)]
        # for i in range(num_rows):
        #     for j in range(num_cols):
        #         if markers[i][j] == CellStatus.MARKED:
        #             model[(num_rows * i) + j] = -model[(num_rows * i) + j]

        warning.config(text='Run {} successfully'.format(algoMode[curMode]), fg='green')
        return# model
    ################################################################################

    def handleRunAlgo(): # Run algorithm to solve the puzzle
        nonlocal stopFlag
        stopFlag = False
        if (curMode == -1):
            warning.config(text='Please select an algorithm!!!', fg='red')
        else:
            changeAllButtonState(DISABLED)
            if (len(matrix) == 0):
                warning.config(text='Please load the puzzle first!!!', fg='red')
                return
            warning.config(text='Running {} .....'.format(algoMode[curMode]), fg='blue')

            model = None
            run = False
            if curMode == Algorithm.PYSAT:
                model = pysat_solution.solve(matrix)
                changeAllButtonState(NORMAL)
                run = True
            elif curMode == Algorithm.A_STAR:
                warning.config(text='{} has not been implemented yet'.format(algoMode[curMode]), fg='red')
                changeAllButtonState(NORMAL)
            elif curMode == Algorithm.BRUTE_FORCE:
                model = brute_force.solve(matrix)
                run = True
            elif curMode == Algorithm.BACKTRACKING:
                if (rtFlag):
                    threading.Thread(target=run_backtracking).start()
                else:
                    model = solve(matrix)
                    changeAllButtonState(NORMAL)
                    run = True
            if run == True:
                if model == None:
                    warning.config(text='No solution with {}'.format(algoMode[curMode]), fg='green')
                else:
                    for widget, num in zip(array.winfo_children(), model):
                        color = 'green' if num > 0 else 'red'
                        widget.config(bg=color, fg='white')
                    warning.config(text='Run {} successfully'.format(algoMode[curMode]), fg='green')

        return
    
    def handleClear(): # Clear puzzle
        warning.config(text='Clearing puzzle .....', fg='blue')
        nonlocal matrix
        nonlocal stopFlag
        stopFlag = True
        for widget in array.winfo_children():
            widget.destroy()
        matrix.clear()
        warning.config(text='Clear puzzle successfully', fg='green')
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
    chooseFile = tk.Button(topRight, text='Choose File', fg='black', command=handleGetFile, width=13)
    chooseFile.pack(pady=5)

    okButton = tk.Button(topRight, text='Load Puzzle', fg='black', command=handleDisplayArray, width=13)
    okButton.pack(pady=5)

    runButton = tk.Button(topRight, text='Run', command=handleRunAlgo, width=13)
    runButton.pack(pady=5)

    clearButton = tk.Button(topRight, text='Clear Puzzle', fg='black', command=handleClear, width=13)
    clearButton.pack(pady=5)

    stopButton = tk.Button(topRight, text="Stop", fg='black', command=handleStop, width=13)
    stopButton.pack(pady=5)

    realtimeToggle = tk.Button(topRight, text="Realtime: OFF", fg='black', command=handleRealtime, width=13)
    realtimeToggle.pack(pady=5)

    # credit = tk.Button(topRight, text='Credit', fg='black', command=handleCredit, width=13)
    # credit.pack(pady=5)

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
        canvas.yview_scroll(int(-1 * (event.delta / ScrollConst.MODIFIER)) , "units")
    canvas.bind_all("<MouseWheel>", scrollWithMouse)

    # Config scroll
    canvas.configure(yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)

    #Create window frame
    canvas.create_window((0, 0), window=array, anchor="nw")

    # Command Infomation (TOP LEFT)
    pathTitle = tk.Label(topLeft, text='Path:')
    filePath = tk.Entry(topLeft, width=50)
    pathTitle.pack(anchor=W)
    filePath.pack()
    algoBlock = tk.Frame(topLeft)
    algoBlock.pack(fill=X)
    algoTitle = tk.Label(algoBlock, text='Selected Algorithm:')
    algoTitle.pack(side=LEFT)
    algoSelected = tk.Label(algoBlock, text='{}'.format(algoMode[curMode]), fg='blue')
    algoSelected.pack(side=LEFT)
    algoButton = tk.Button(algoBlock, text='Select Algorithm', fg='black', command=handleSelectAlgo, width=13)
    algoButton.pack(side=RIGHT, pady=10)

    # Notification while running
    mid = tk.LabelFrame(topLeft, text="Status")
    mid.pack(side=BOTTOM, fill=X)
    warning = tk.Label(mid, text='None', fg='black')
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
    root.geometry('%dx%d+%d+%d' % (width, height, root.winfo_screenwidth() / 2 - width / 2, root.winfo_screenheight() / 2 - height / 2))
    root.update()
    root.mainloop()