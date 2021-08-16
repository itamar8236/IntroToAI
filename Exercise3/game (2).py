# Itamar Cohen 318558236 &
# Avraham Glasberg 206218745
import copy
import alphaBetaPruning
import random

VICTORY = 10 ** 20  # The value of a winning board (for max)
LOSS = -VICTORY  # The value of a losing board (for max)
TIE = 0  # The value of a tie
SIZE = 4  # the length of winning seq.
COMPUTER = SIZE + 1  # Marks the computer's cells on the board
HUMAN = 1  # Marks the human's cells on the board

rows = 6
columns = 7


# class for representing the game, include board, size of empty cells, turn
class game:
    board = []
    size = rows * columns
    playTurn = HUMAN

    # Used by alpha-beta pruning to allow pruning

    '''
    The state of the game is represented by a list of 4 items:
        0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
        the comp's cells = COMPUTER and the human's = HUMAN
        1. The heuristic value of the state.
        2. Whose turn is it: HUMAN or COMPUTER
        3. Number of empty cells
    '''


# create the game (parameter s) field for init game
def create(s):
    # Returns an empty board. The human plays first.
    # create the board
    s.board = []
    for i in range(rows):
        s.board = s.board + [columns * [0]]

    s.playTurn = HUMAN
    s.size = rows * columns
    s.val = 0.00001

    # return [board, 0.00001, playTurn, r*c]     # 0 is TIE


#  make new instance of object game as copy of the current
def cpy(s1):
    # construct a parent DataFrame instance
    s2 = game()
    s2.playTurn = s1.playTurn
    s2.size = s1.size
    s2.board = copy.deepcopy(s1.board)
    # print("board ", s2.board)
    return s2


'''
We fixed the bug that was in the original code,
that didn't break of the loop in case of lose or victory.
Now, when the functions finds 4 in a row, it stops its calculation and return loss/victory value.
In addition we added few changes in order to improve the efficiency of the value function.
First, we gave different value to different length of elements. Instead of 1 for the agent and -1 
for the other player, we gave 2 for 2 in a row and 3 for 3 in a row (negative if it's the opponent row)
The change is in the CheckSeq function
In addition, we add another calculation in a new function (checkIfNextWin) that checks whether or not the
4 given squares (that sent to CheckSeq function) are near complete, meaning, it is possible to complete the 4 
in a row in the next turn. the amount of 3's like that are saved in the value function, and added to the final
value, of course, every additional 'close win' is with very hugh value, so we used the power function(**)
in order to calculate that. we powered the number in the power of 5, in order to it to remain negative
in case the close wins are the opponent's.
'''


def value(s):
    # Returns the heuristic value of s
    dr = [-SIZE + 1, -SIZE + 1, 0, SIZE - 1]  # the next lines compute the heuristic val.
    dc = [0, SIZE - 1, SIZE - 1, SIZE - 1]
    #  represent zero but with epsilon for distinguish from the zero of TIE state
    val = 0.00001
    nextWins = 0
    #  the breaks happened when the value is LOSS/VICTORY because that determine the state value
    for row in range(rows):
        if val in [LOSS, VICTORY]:
            break
        for col in range(columns):
            if val in [LOSS, VICTORY]:
                break
            # check the val of each cell in the board
            for i in range(len(dr)):
                t, t2 = checkSeq(s, row, col, row + dr[i], col + dc[i])
                nextWins += t2
                if t in [LOSS, VICTORY]:
                    val = t
                    # will break from all the loop by the another breaks above
                    break
                else:
                    # calculate the sum of all the cases in the current state
                    val += t
    if s.size == 0 and val not in [LOSS, VICTORY]:
        val = TIE
    #  our important extension for bring nextWins significant value
    if val not in [LOSS, VICTORY, TIE]:
        val += nextWins ** 5 * 5
    return val


# check the sequence of specific state
def checkSeq(s, r1, c1, r2, c2):
    # r1, c1 are in the board. if r2,c2 not on board returns 0.
    # Checks the seq. from r1,c1 to r2,c2. If all X returns VICTORY. If all O returns LOSS.
    # If empty returns 0.00001. If no Os returns 1. If no Xs returns -1.
    if r2 < 0 or c2 < 0 or r2 >= rows or c2 >= columns:
        return 0, 0  # r2, c2 are illegal

    dr = (r2 - r1) // (SIZE - 1)  # the horizontal step from cell to cell
    dc = (c2 - c1) // (SIZE - 1)  # the vertical step from cell to cell

    sum = 0

    for i in range(SIZE):  # summing the values in the seq.
        sum += s.board[r1 + i * dr][c1 + i * dc]

    if sum == COMPUTER * SIZE:
        return VICTORY, 0
    elif sum == HUMAN * SIZE:
        return LOSS, 0
    # we prefer to use the numbers themself (2,3) instead of using SIZE - 1, SIZE - 2 etc'
    # improving the heuristic by checking the number of elements in a row.
    elif sum > 0 and sum < COMPUTER:
        if sum == 3:
            return -3, -1 * checkIfNextWin(s, r1, c1, r2, c2)
        return -1 * sum, 0

    elif sum > 0 and sum % COMPUTER == 0:
        if sum // COMPUTER == 3:
            return 3, checkIfNextWin(s, r1, c1, r2, c2)
        return 1 * (sum // COMPUTER), 0
    return 0.00001, 0  # not 0 because TIE is 0


# finding if in the specific 4 cell there is option to win in the next step
def checkIfNextWin(s, r1, c1, r2, c2):
    dr = (r2 - r1) // (SIZE - 1)  # the horizontal step from cell to cell
    dc = (c2 - c1) // (SIZE - 1)  # the vertical step from cell to cell

    for i in range(SIZE):  # summing the values in the seq.
        if s.board[r1 + i * dr][c1 + i * dc] == 0:
            if r1 + i * dr == 5 or s.board[(r1 + i * dr) + 1][c1 + i * dc] != 0:
                return 1
    return 0


# print the board of the state
def printState(s):
    # Prints the board. The empty cells are printed as numbers = the cells name(for input)
    # If the game ended prints who won.
    for r in range(rows):
        print("\n|", end="")
        for c in range(columns):
            if s.board[r][c] == COMPUTER:
                print("X|", end="")
            elif s.board[r][c] == HUMAN:
                print("O|", end="")
            else:
                print(" |", end="")
    print()

    for i in range(columns):  # For numbers on the bottom
        print(" ", i, sep="", end="")

    print()
    # check and print the result of the game
    val = value(s)

    if val == VICTORY:
        print("I won!")
    elif val == LOSS:
        print("You beat me!")
    elif val == TIE:
        print("It's a TIE")


# check if the game finished
def isFinished(s):
    # Seturns True iff the game ended
    return value(s) in [LOSS, VICTORY, TIE] or s.size == 0


# check if now it is the turn of the Human
def isHumTurn(s):
    # Returns True iff it is the human's turn to play
    return s.playTurn == HUMAN


# ask the user to choose who is first in the turns
def decideWhoIsFirst(s):
    # The user decides who plays first
    if int(input("Who plays first? 1-me / anything else-you : ")) == 1:
        s.playTurn = COMPUTER
    else:
        s.playTurn = HUMAN
    return s.playTurn


# make legal move
def makeMove(s, c):
    # Puts mark (for human or computer) in col. c
    # and switches turns.
    # Assumes the move is legal.
    r = 0
    while r < rows and s.board[r][c] == 0:
        r += 1

    s.board[r - 1][c] = s.playTurn  # marks the board
    s.size -= 1  # one less empty cell
    if (s.playTurn == COMPUTER):
        s.playTurn = HUMAN
    else:
        s.playTurn = COMPUTER


# Reads, enforces legality and executes the user's move.
def inputMove(s):
    flag = True
    while flag:
        c = int(input("Enter your next move: "))
        if c < 0 or c >= columns or s.board[0][c] != 0:
            print("Illegal move.")
        else:
            flag = False
            makeMove(s, c)


# make random move,if no obvious move
def inputRandom(s):
    # See if the random should block one move ahead
    '''for i in range(0,columns):
        tmp=cpy(s)
        makeMove(tmp, i)
        if(value(tmp)==VICTORY):
            makeMove(s,i)'''
    for i in range(0, columns):  # this simple agent always plays min
        tmp = cpy(s)
        makeMove(tmp, i)
        if (value(tmp) == LOSS and s.board[0][i] == 0):  # so a "loss" is a win for this side
            makeMove(s, i)
            return
    # If no obvious move, than move random
    flag = True
    while flag:
        c = random.randrange(0, columns)
        if c < 0 or c >= columns or s.board[0][c] != 0:
            print("Illegal move.")
            printState(s)
            # break
        else:
            flag = False
            makeMove(s, c)


# makes and return list of the next options states
def getNext(s):
    # returns a list of the next states of s
    ns = []
    for c in list(range(columns)):
        # print("c=",c)
        if s.board[0][c] == 0:
            # print("possible move ", c)
            tmp = cpy(s)
            makeMove(tmp, c)
            # print("tmp board=",tmp.board)
            ns += [tmp]
            # print("ns=",ns)
    return ns


# make move by using alpha Beta Pruning algorithm
def inputComputer(s):
    return alphaBetaPruning.go(s)
