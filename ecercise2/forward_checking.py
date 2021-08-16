# Avraham Glasberg and Itamar Cohen
# implementation of forward checking:
import numpy as np # 2 dim array - for saving the board

columns = [] #columns is the locations for each of the queens
size = 15 # size of the board
board = np.zeros((size, size)) # init of the board

def display(): # display the board
    for row in range(len(columns)):
        for column in range(size):
            if column == columns[row]:
                print('♛', end=' ')
            else:
                print(' .', end=' ')
        print()

# this func finding solution for the n queen problem using forward checking method:
def solve_queen(size):
    columns.clear() # init the list of queen in column
    # init the feild for the func:
    number_of_moves = 0
    number_of_iterations = 0
    row = 0
    column = 0
    # iterate over rows of board
    while True:
        # place queen in next row
        while column < size: # more queen should be insert to the board
            number_of_iterations += 1 # counter
            if board[row][column] == 0: # check if the place is ok to insert
                place_in_next_row(row, column) # add the queen to board
                number_of_moves += 1 # counter
                row += 1 # move to the next row
                column = 0 # starting from the first col in the row
                break
            else: # the current place isn't ok, move to the next one
                column += 1
        # if I could not find an open column or if board is full or the last adding queen block some row in the countiones of the board
        if (column == size or row == size or is_block_row(row)):
            number_of_iterations += 1
            # if board is full, we have a solution
            if row == size:
                print("I did it! Here is my solution")
                display()
                # print(number_of_moves)
                return number_of_iterations, number_of_moves
            # I couldn't find a solution so I now backtrack
            prev_column = remove_in_current_row()
            number_of_moves += 1
            if (prev_column == -1):  # I backtracked past column 1
                print("There are no solutions")
                return number_of_iterations, number_of_moves
            # try previous row again
            row -= 1
            # start checking at column = (1 + value of column in previous row)
            column = 1 + prev_column

def is_block_row(row): # check that the next rows not blocked
    for i in range(row + 1, size):
        lst = []
        for j in range(size):
           lst.append(board[i][j])
        if not(0 in lst):
            return True
    return False

#placing queen in location
def place_in_next_row(row, column):
    columns.append(column)
    update_board(row, column, 1)

#update board with all threats from the new queen
def update_board(row, column, num):
    # vertical & horizontical
    for i in range(size):
        board[i][column] += num
    # 4 loops for :
    # top right places
    for i in range(size):
        board[row][i] += num

    tc = column + 1
    tr = row + 1
    while tc < size and tr < size:
        board[tr][tc] += num
        tc += 1
        tr += 1

    # down top places
    tc = column + 1
    tr = row - 1
    while tc < size and tr >= 0:
        board[tr][tc] += num
        tc += 1
        tr -= 1

    # back up places
    tc = column - 1
    tr = row + 1
    while tc >= 0 and tr < size:
        board[tr][tc] += num
        tc -= 1
        tr += 1

    # back down places
    tc = column - 1
    tr = row - 1
    while tc >= 0 and tr >= 0:
        board[tr][tc] += num
        tc -= 1
        tr -= 1

    # the queen's place
    board[row][column] = 0

#remove last queen
def remove_in_current_row():
    if len(columns) > 0:
        column = columns.pop()
        row = len(columns)
        update_board(row, column, -1)
        return column
    return -1

# running the func on the size that define at the head of the file:
iter, sum = solve_queen(size)
print("# of iterations:", iter)
print("# of queens placed + backtracks:", sum)
print(columns)
