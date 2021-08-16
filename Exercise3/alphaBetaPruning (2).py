# Itamar Cohen 318558236 &
# Avraham Glasberg 206218745
import game

# Depth of the search in the alpha beta algorithm
DEPTH = 2


# turn function. checks the best next move.
# The function checks who's turn is, and used MinMax algorithm with alpha beta to find the nest next move.
def go(gm):
    # print("In go of game ", gm.board)
    if game.isHumTurn(gm):
        # print("Turn of human")
        obj = abmin(gm, DEPTH, game.LOSS - 1, game.VICTORY + 1)[1]
        # print("object board: ",obj.board)
        return obj
    else:
        # print("Turn of agent")
        obj = abmax(gm, DEPTH, game.LOSS - 1, game.VICTORY + 1)[1]
        # print("object board: ",obj.board)
        return obj


'''
The MinMax algorithm checks the best next move, by checking the value of each current state of the board,
and when the maximum value is always best for the agent (me) and the minimal value is worst for the agent and
best for it's opponent. (because it is sum-zero game)
in our case, the function above (go) checks who's turn is it. if it's the Computer's turn (the agent's) the function 
calls abmax function that return the highest value state, and abmin otherwise, that returns the lowest value state,
which as i mentioned is best for the agent's opponent. abmax & abmin works based on the same algorithm only return
the opposite values.
In our case, (Depth = 2, 4 in a row game) the algorithm "thinks" 2 steps ahead,
and calculate all the options there, than calculate what's 
my opponent will do, based on the the value of the states, then from those options he picks the best state for me
(highest for the agent and lowest for the opponent)
To calculate that, the algorithm calls the functions abmax and abmin in recursion.
The algorithm also uses alphabeta algorithm, but it is not mentioned in the question to elaborate about it,
in short - because my opponent always picks the best moves for him, we can 'cut' the tree if v we found is >=
in max node or <= in min node.
The algorithm goes in depth 2 by calling all the next possible states which are provided by getNext function,
the function calculate and return all the possible next states the game can be in
(max 7 states, for every column, and 1 down for every full column).
The algorithm assume the value function is well written and calculate well the value of a current state. 
we explain about our changes and strategy in the relevant location
'''


# s = the state (max's turn)
# d = max. depth of search
# a,b = alpha and beta
# returns [v, ns]: v = state s's value. ns = the state after recomended move.
#        if s is a terminal state ns=0.
def abmax(gm, d, a, b):
    # print("now calculate abmax")
    # print("d=",d)
    # print("alpha=",a)
    # print("beta=",b)
    if d == 0 or game.isFinished(gm):
        # search is over - depth 0 or game is finished, the function returns the final value.
        # print("returns ", [game.value(gm), gm])
        return [game.value(gm), gm]
    v = float("-inf")
    ns = game.getNext(gm)
    # possible next moves (max 7, one down by every full column as i explained before.
    # print("next moves:", len(ns), " possible moves ")
    bestMove = 0
    for st in ns:
        tmp = abmin(st, d - 1, a, b)
        if tmp[0] > v:
            v = tmp[0]
            bestMove = st
        if v >= b:
            return [v, st]
        if v > a:
            a = v
    return [v, bestMove]


# s = the state (min's turn)
# d = max. depth of search
# a,b = alpha and beta
# returns [v, ns]: v = state s's value. ns = the state after recomended move.
#        if s is a terminal state ns=0.
def abmin(gm, d, a, b):
    # print("now calculate abmin")
    # print("d=",d)
    # print("a=",a)
    # print("b=",b)

    if d == 0 or game.isFinished(gm):
        # same idea as abmax
        # print("returns ", [game.value(gm), gm])
        return [game.value(gm), 0]
    v = float("inf")

    ns = game.getNext(gm)
    # same idea as i explained
    # print("next moves:", len(ns), " possible moves ")
    bestMove = 0
    for st in ns:
        tmp = abmax(st, d - 1, a, b)
        if tmp[0] < v:
            v = tmp[0]
            bestMove = st
        if v <= a:
            return [v, st]
        if v < b:
            b = v
    return [v, bestMove]
