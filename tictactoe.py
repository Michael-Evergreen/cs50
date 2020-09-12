"""
Tic Tac Toe Player
"""
import copy
import math
import numpy as np

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    arr = np.array(board)[0:3, 0:3]

    if np.count_nonzero(arr == X) <= np.count_nonzero(arr == O):
        return X
    elif np.count_nonzero(arr == O) < np.count_nonzero(arr == X):
        return O




def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                possible_actions.add((row, col))

    return possible_actions




def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copiedboard = copy.deepcopy(board)
    current_player = player(board)
    for row in range(3):
        for col in range(3):
            if (row, col) == action:
                copiedboard[row][col] = current_player
    return copiedboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        n = row[0]
        if n != EMPTY and row.count(n) == 3:
            return n

    for col in range(3):
        g = np.array(board)[0:3, col]
        m = board[0][col]
        if np.count_nonzero(g == m) == 3 and m != EMPTY:
            return m

    f = board[1][1]
    if (f != EMPTY and f == board[0][0] and f == board[2][2]) or (f != EMPTY and f == board[0][2] and f == board[2][0]):
        return f




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if board[0].count(EMPTY) == board[1].count(EMPTY) == board[2].count(EMPTY) == 0:
        return True
    if winner(board) != None:
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    kq = winner(board)
    if kq == X:
        return 1
    if kq == O:
        return -1
    if kq == None:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        possible_actions = actions(board)
        action_result_value = {}
        for action in possible_actions:
            action_result_value[action] = min_value(result(board, action))
        maxaction = max(action_result_value, key=action_result_value.get)
        return maxaction

    if player(board) == O:
        possible_actions = actions(board)
        action_result_value = {}
        for action in possible_actions:
            action_result_value[action] = max_value(result(board, action))
        minaction = min(action_result_value, key=action_result_value.get)
        return minaction
    """
    MAX Pick an action "a" in possible actions that produces highest value of MIN-Value(Result(s, a))
    
    """





def max_value(board):
    if terminal(board):
        return utility(board)
    v = -10
    array = []
    for action in actions(board):
        array.append(min_value(result(board, action)))
        array.append(v)
        v = max(array)
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = 10
    array =[]
    for action in actions(board):
        array.append(max_value(result(board, action)))
        array.append(v)
        v = min(array)
    return v
