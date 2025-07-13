import tkinter as tk
# First Page Function
def start_page():
    root = tk.Tk()
    root.title("Welcome")
    root.geometry("400x400")
    root.configure(bg="#f0f8ff")

    # Title Label
    tk.Label(root, text="🧩 Welcome to Sudoku Solver 🧠", font=("Comic Sans MS", 18, "bold"),
             bg="#f0f8ff", fg="#1a1aff").pack(pady=50)

    # Subtext
    tk.Label(root, text="Click below to get started!", font=("Helvetica", 12),
             bg="#f0f8ff", fg="gray").pack(pady=10)

    # Start Button
    start_btn = tk.Button(root, text="🚀 Start Sudoku Solver", font=("Arial", 14, "bold"),
                          bg="#4CAF50", fg="black", padx=20, pady=10,
                          command=lambda: [root.destroy(), sudoku_solver()])
    start_btn.pack(pady=30)

    root.mainloop()

# Second Page (Solver GUI)
def sudoku_solver():
    root = tk.Tk()
    root.title("Sudoku Solver")
    root.geometry("500x580")

    tk.Label(root, text="🧠 Fill the Sudoku and Click Solve", font=("Arial", 16, "bold")).grid(row=0, column=1, columnspan=10, pady=10)

    errLabel = tk.Label(root, text="", fg="red", font=("Arial", 16))
    errLabel.grid(row=15, column=1, columnspan=10, pady=5)

    solvedLabel = tk.Label(root, text="", fg="green", font=("Arial", 16, "bold"))
    solvedLabel.grid(row=16, column=1, columnspan=10, pady=5)

    cells = {}

    def ValidateNumber(P):
        return (P.isdigit() or P == "") and len(P) < 2
    reg = root.register(ValidateNumber)

    def draw3x3Grid(row, column, bgcolor):
        for i in range(3):
            for j in range(3):
                e = tk.Entry(root, width=5, bg=bgcolor, fg="black", font=("Arial", 14, "bold"),
                             justify="center", bd=2, relief="ridge", validate="key", validatecommand=(reg, "%P"))
                e.grid(row=row + i + 1, column=column + j + 1, sticky="nsew", padx=1, pady=1, ipady=5)
                cells[(row + i + 1, column + j + 1)] = e

    def draw9x9Grid():
        color = "#e6f7ff"
        for rowNo in range(1, 10, 3):
            for colNo in range(0, 9, 3):
                draw3x3Grid(rowNo, colNo, color)
                color = "#fff2cc" if color == "#e6f7ff" else "#e6f7ff"

    def clearValues():
        errLabel.config(text="")
        solvedLabel.config(text="")
        for row in range(2, 11):
            for col in range(1, 10):
                cells[(row,col)].delete(0,tk.END)

    def getValues():
        board = []
        errLabel.config(text="")
        solvedLabel.config(text="")
        for row in range(2, 11):
            rows = []
            for col in range(1, 10):
                val = cells[(row, col)].get()
                if val == "":
                    rows.append(0)
                elif val.isdigit() and 1 <= int(val) <= 9:
                    rows.append(int(val))
                else:
                    errLabel.config(text="❌ Invalid input! Please enter numbers 1-9.")
                    return
            board.append(rows)

        if not is_valid_puzzle(board):
            errLabel.config(text="❌ Invalid puzzle. Please check your numbers.")
            return

        if solve_sudoku(board):
            update_grid(board)
            solvedLabel.config(text="✅ Sudoku Solved!")
        else:
            errLabel.config(text="❌ No solution exists!")

    def is_valid_puzzle(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] != 0:
                    if not is_valid(board, row, col, board[row][col]):
                        return False
        return True

    def is_valid(board, row, col, num):
        for i in range(9):
            if (board[row][i] == num and i != col) or (board[i][col] == num and i != row):
                return False
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if board[r][c] == num and (r, c) != (row, col):
                    return False
        return True

    def solve_sudoku(board):
        empty = find_empty_location(board)
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if is_valid(board, row, col, num):
                board[row][col] = num
                if solve_sudoku(board):
                    return True
                board[row][col] = 0
        return False

    def find_empty_location(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return row, col
        return None
    def update_grid(board):
        for row in range(9):
            for col in range(9):
                cells[(row + 2, col + 1)].delete(0, tk.END)
                if board[row][col] != 0:
                    cells[(row + 2, col + 1)].insert(0, str(board[row][col]))


    
    solveBtn = tk.Button(root, command=getValues, text="Solve", width=10, bg="green", fg="black", font=("Arial", 12, "bold"))
    solveBtn.grid(row=20, column=1, columnspan=5, pady=10)

    clearBtn = tk.Button(root, command=clearValues, text="Clear", width=10, bg="red", fg="black", font=("Arial", 12, "bold"))
    clearBtn.grid(row=21, column=1, columnspan=5, pady=5)

    exitBtn = tk.Button(root, command=root.destroy, text="Exit", width=10, bg="gray", fg="black", font=("Arial", 12, "bold"))
    exitBtn.grid(row=22, column=1, columnspan=5, pady=5)

    draw9x9Grid()
    root.mainloop()

# Run the start page first
start_page()
