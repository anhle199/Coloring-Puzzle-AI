import tkinter as tk
from tkinter.constants import DISABLED, LEFT, NORMAL, RIGHT, X, END
from tkinter.filedialog import askopenfilename
from utilities.file_io import *
from utilities.constants import CellStatus, CellSize, Algorithm
import pysat_solution
import backtracking
import brute_force


def GUI():
    root = tk.Tk()
    root.title('Coloring Puzzle - AI HCMUS')
    top = tk.Frame(root)
    top.pack(pady=10)
    mid = tk.Frame(root)
    mid.pack(fill=X, padx=10, pady=5)
    bot = tk.Frame(root)
    bot.pack()

    # variables
    algoMode = ['PySat', 'A Star', 'Brute Force', 'Backtracking', 'None']
    curMode = -1
    matrix = []

    def handleGetFile():
        path = askopenfilename()
        filePath.delete(0, END)
        filePath.insert(0, path)
        return

    def handleCredit():
        popup = tk.Tk()
        popup.title('Credit')
        creditText = tk.Label(popup, text='Project 2: Coloring Puzzle', font=('Arial', 15))
        creditText.pack(padx=10, pady=10)
        creditTextBody1 = tk.Label(popup, text='Programmed by:', font=('Arial', 10))
        creditTextBody1.pack()
        creditTextBody2 = tk.Label(popup, text='Nguyen Hua Hung - 19127150\nLe Minh Huy - 19127157\nLe Hoang Anh - 19127329')
        creditTextBody2.pack(padx=10, pady=5)
        creditTextFooter = tk.Label(popup, text='University Of Science - HCM City', font=('Arial', 10))
        creditTextFooter.pack(padx=10, pady=10)
        popup.geometry('300x200+%d+%d' % (root.winfo_screenwidth() / 2 - 150, root.winfo_screenheight() / 2 - 100))
        return

    def handleDisplayArray():
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
            return
        except ValueError:
            warning.config(text='File does not exist!!!!', fg='red')
            return

        width = root.winfo_width()
        height = root.winfo_height()
        hSum = 0
        wSum = 0
        for i in range(size[0]):
            h = 0
            w = 0
            for j in range(size[1]):
                cell = ' '
                if matrix[i][j] != -1:
                    cell = str(matrix[i][j])
                box = tk.Label(array, text=cell, width=CellSize.WIDTH, height=CellSize.HEIGHT, borderwidth=2, relief='solid', font=('Arial', 20))
                box.grid(row=i, column=j)
                box.update()
                h = box.winfo_height()
                w += box.winfo_width()
            hSum += h
            wSum = w
        if wSum > width:
            width += wSum - width + 20
        if hSum > height - 100:
            height += hSum - height + root.winfo_height() + 20

        root.geometry('%dx%d+%d+%d' % (width, height, root.winfo_screenwidth() / 2 - width / 2, root.winfo_screenheight() / 2 - (height + 10) / 2))

        warning.config(text='Load successfully', fg='green')
        okButton['state'] = NORMAL
        return

    def handleSelectAlgo():
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
            ('Brute Force', '2'),
            ('Backtracking', '3')
            # ('PySat', str(Algorithm.PYSAT)),
            # ('A Star', str(Algorithm.A_STAR)),
            # ('Brute Force', str(Algorithm.BRUTE_FORCE)),
            # ('Backtracking', str(Algorithm.BACKTRACKING))
        )
        def onClick():
            return
        def handleConfirm():
            nonlocal curMode
            curMode = int(mode.get())
            algoTitle.config(text='Selected Algorithm: {}'.format(algoMode[curMode]))
            popup.destroy()
        i = 0
        for item in values:
            tk.Radiobutton(optionWrapper, text=item[0], variable=mode, value=item[1], command=onClick).grid(row=0, column=i)
            i += 1
        # confirmButton = tk.Button(popup, text='Confirm', command=handleConfirm, background='green', fg='white')
        confirmButton = tk.Button(popup, text='Confirm', command=handleConfirm)
        confirmButton.pack(side=RIGHT, padx=10)
        popup.geometry('450x150+%d+%d' % (root.winfo_screenwidth() / 2 - 225, root.winfo_screenheight() / 2 - 75))
        return

    def handleRunAlgo():
        if (curMode == -1):
            warning.config(text='Please select an algorithm!!!', fg='red')
        else:
            warning.config(text='Running {} ...'.format(algoMode[curMode]), fg='blue')

            model = None
            if curMode == Algorithm.PYSAT:
                model = pysat_solution.solve(matrix)
            elif curMode == Algorithm.A_STAR:
                warning.config(text='Not implemented {} yet'.format(algoMode[curMode]), fg='red')
            elif curMode == Algorithm.BRUTE_FORCE:
                model = brute_force.solve(matrix)
            elif curMode == Algorithm.BACKTRACKING:
                model = backtracking.solve(matrix)

            if model == None:
                warning.config(text='No solution with {}'.format(algoMode[curMode]), fg='green')
            else:
                for widget, num in zip(array.winfo_children(), model):
                    color = 'green' if num > 0 else 'red'
                    widget.config(bg=color, fg='white')
                warning.config(text='Run {} successfully'.format(algoMode[curMode]), fg='green')

        return

    topLeft = tk.Frame(top, width=200, height=100)
    topLeft.pack(side=LEFT, padx=10)
    topRight = tk.Frame(top, width=200, height=100)
    topRight.pack(side=RIGHT, padx=10)

    chooseFile = tk.Button(topRight, text='Choose File', fg='black', command=handleGetFile, width=13)
    chooseFile.pack(pady=5)

    okButton = tk.Button(topRight, text='Load Puzzle', fg='black', command=handleDisplayArray, width=13)
    okButton.pack(pady=5)

    # runButton = tk.Button(topRight, text='Run', bg='green', fg='white', command=handleRunAlgo, width=13)
    runButton = tk.Button(topRight, text='Run', command=handleRunAlgo, width=13)
    runButton.pack(pady=5)

    credit = tk.Button(topRight, text='Credit', fg='black', command=handleCredit, width=13)
    credit.pack(pady=5)

    status = tk.Label(mid, text='Notification:')
    status.pack(side=LEFT)
    warning = tk.Label(mid, text='None', fg='black')
    warning.pack(side=LEFT)

    array = tk.Frame(bot)
    array.pack()

    pathTitle = tk.Label(topLeft, text='Path', justify=LEFT)
    filePath = tk.Entry(topLeft, width=50)
    pathTitle.pack()
    filePath.pack()
    algoTitle = tk.Label(topLeft, text='Selected Algorithm: {}'.format(algoMode[curMode]))
    algoTitle.pack(side=LEFT)
    algoButton = tk.Button(topLeft, text='Select Algorithm', fg='black', command=handleSelectAlgo, width=13)
    algoButton.pack(side=RIGHT, pady=10)

    top.update()
    mid.update()
    root.geometry('%dx%d+%d+%d' % (top.winfo_width(), top.winfo_height() + mid.winfo_height() + 30, root.winfo_screenwidth() / 2 - top.winfo_width() / 2, root.winfo_screenheight() / 2 - (top.winfo_height() + mid.winfo_height() + 30) / 2))
    root.update()
    root.mainloop()