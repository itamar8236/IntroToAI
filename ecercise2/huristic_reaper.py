# Avraham Glasberg and Itamar Cohen

"""Huristic repair. we used the previous algorithm (forward checking) and added random select for the next column, which imprives the running time significally"""
import numpy as np # 2 dim array - for saving the board
import random

columns = [] #columns is the locations for each of the queens
size = 15 # size of the board
board = np.zeros((size, size)) # init the board of zeroes

def display(): # display the board
    for row in range(len(columns)):
        for column in range(size):
            if column == columns[row]:
                print('♛', end=' ')
            else:
                print(' .', end=' ')
        print()


def solve_queen(size): #solving the queen's problem. return the number of iterations and queens placing & backtracking
    columns.clear()
    clear_data()
    number_of_moves = 0
    number_of_iterations = 0
    row = 0
    column = next_column(row)
    while True:
        # place queen in next row
        ''''print(columns)
        print("I have ", row, " number of queens put down")
        display()
        print(number_of_moves)'''
        while column > -1:
            number_of_iterations += 1
            if board[row][column] == 0:
                place_in_next_row(row, column)
                number_of_moves += 1
                row += 1
                column = next_column(row)
                break
            else:
                column = next_column(row)
        # if I could not find an open column or if board is full
        if (column == -1 or row == size or is_block_row(row)):
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
                # print(number_of_moves)
                return number_of_iterations, number_of_moves
            # try previous row again
            for i in range(size): #clearing pplaces forbidden for backtracking queens
                if board[row][i] == -1:
                    board[row][i] = 0
            row -= 1
            board[row][prev_column] = -1 #to prevent queen to be here
            column = next_column(row)

#clear the board
def clear_data():
    for i in range(size):
        for j in range(size):
            board[i][j] = 0

#random select the next place for the column from the possible locations. return -1 if there is none
def next_column(row):
    if row >= size:
        return -1
    l = []
    for j in range(size):
        if board[row][j] == 0:
            l.append(j)
    if not(l):
        return -1
    return random.choice(l)


#checking if threre is blocked row - which means that we need to backtrack
def is_block_row(row):
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
    #vertical & horizontical
    for i in range(size):
        board[i][column] += num

    for i in range(size):
        board[row][i] += num

    #4 loops for :
    #top right places
    tc = column + 1
    tr = row + 1
    while tc < size and tr < size:
        board[tr][tc] += num
        tc += 1
        tr += 1

    #down top places
    tc = column + 1
    tr = row - 1
    while tc < size and tr >= 0:
        board[tr][tc] += num
        tc += 1
        tr -= 1

    #back up places
    tc = column - 1
    tr = row + 1
    while tc >= 0 and tr < size:
        board[tr][tc] += num
        tc -= 1
        tr += 1

    #back down places
    tc = column - 1
    tr = row - 1
    while tc >= 0 and tr >= 0:
        board[tr][tc] += num
        tc -= 1
        tr -= 1

    #the queen's place
    board[row][column] = 0

#remove last queen
def remove_in_current_row():
    if len(columns) > 0:
        column = columns.pop()
        row = len(columns)
        update_board(row, column, -1)
        return column
    return -1

#sum = 0, iter = 0
#for i in range(0, 100):
#columns = [] #columns is the locations for each of the queens
def main12():
    number_of_iterations = 0
    num_of_moves = 0
    for j in range(20):#average of 20 runs of size of 28
        print(j)
        iter, sum = solve_queen(size)
        number_of_iterations += iter
        num_of_moves += sum

    print("Number of iterations for board in size " + str(size) + " is: " + str(number_of_iterations / 20))
    print("# of queens placed + backtracks:", num_of_moves/20)

#run main12
main12()

