"""
Tic Tac Toe Player
"""

import math
import copy

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
    numberofx = 0
    numberofo = 0
    
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == X:
                numberofx += 1
            if board[row][column] == O:
                numberofo += 1
    if numberofx > numberofo:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleMoves = set()
    
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == EMPTY:
                possibleMoves.add((row, column))
    
    return possibleMoves            


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid move")
    
    copy_board = copy.deepcopy(board)

    row, column = action
    copy_board[row][column] = player(board)
    return copy_board


def row_check(board, player):
    for row in range(len(board)):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    return False

def column_check(board, player):
    for column in range(len(board)):
        if board[column][0] == player and board[column][1] == player and board[column][2] == player:
            return True
    return False

def diagonal_check(board, player):
    checker = 0
    for row in range(len(board)):
        for column in range(len(board)):
            if row == column and board[row][column] == player:
                checker += 1
    if checker == 3:
        return True
    else: 
        return False
    

def diagonal2_check(board, player):
    checker = 0
    for row in range(len(board)):
        for column in range(len(board)):
            if (len(board) - row - 1) == column and board[row][column] == player:
                checker += 1
    if checker == 3:
        return  True
    else:
        return False       


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """ 
    if row_check(board, X) or column_check(board, X) or diagonal_check(board, X) or diagonal2_check(board, X):
        return X 
    elif row_check(board, O) or column_check(board, O) or diagonal_check(board, O) or diagonal2_check(board, O):
        return O
    else: 
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X:
        return True
    if winner(board) == O:
        return True
    for row in range(len(board)):
        for column in range(len(board)):
            if board[row][column] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    else:
        return 0

def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v
        
def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    elif player(board) == X:
        moves = []
        for action in actions(board):
            moves.append([min_value(result(board, action)), action])
        return sorted(moves, key=lambda x: x[0], reverse=True)[0][1]

    elif player(board) == O:
        moves = []
        for action in actions(board):
            moves.append([max_value(result(board, action)), action])
        return sorted(moves, key=lambda x: x[0])[0][1]
