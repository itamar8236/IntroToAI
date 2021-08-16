# Avraham Glasberg and Itamar Cohen
# implementation of British museum :

columns = []  # columns is the locations for each of the queens
# columns[r] is a number c if a queen is placed at row r and column c.
size = 4
import random

# place queens in board
def place_n_queens(size): # place queens in board
    columns.clear()
    row = 0
    while row < size:
        column = random.randrange(0, size)
        columns.append(column)
        row += 1

# display the board
def display():
    for row in range(len(columns)):
        for column in range(size):
            if column == columns[row]:
                print('♛', end=' ')
            else:
                print(' .', end=' ')
        print()

# check board correction
def is_solution():
    for queen_row1, queen_column1 in enumerate(columns):
        if not (is_safe(queen_row1, queen_column1)):
            return False
    return True

# check the square correction
def is_safe(row, column):
    for queen_row, queen_column in enumerate(columns):
        if column == queen_column and not (row == queen_row):
            return False

    # check diagonal
    for queen_row, queen_column in enumerate(columns):
        if queen_column - queen_row == column - row and not (column == queen_column and row == queen_row):
            return False

    # check other diagonal
    for queen_row, queen_column in enumerate(columns):
        if ((size - queen_column) - queen_row == (size - column) - row) and not (
                column == queen_column and row == queen_row):
            return False
    return True

# run the solution 20 times and print the avg
def british():
    number_of_iterations = 0
    for j in range(20):
        for i in range(1000000):
            place_n_queens(size)
            if is_solution():
                number_of_iterations += i
                break
    print()
    print("Number of iterations for board in size " + str(size) + " is: " + str(number_of_iterations/20))

british()
