import random
import math

scores = {
    'p': 1,
    'n': 3,
    'b': 3,
    'r': 5,
    'q': 9,
    'k': 1
}

depth = 3

def move(board):
    maximizing = board.turn() == 'w'
    (value, best) = minimax(board, depth, maximizing)
    print(value, best)
    return best

def features(board, player):
    do = None

def evaluate(board):
    w_pieces = board.get_pieces(lambda p: p._color == 'w')
    b_pieces = board.get_pieces(lambda p: p._color != 'w')

    w_score = list(map(lambda p: scores[p._symbol], w_pieces))
    b_score = list(map(lambda p: scores[p._symbol], b_pieces))

    return sum(w_score) - sum(b_score)

def minimax(board, depth, maximizing):
    if depth < 1:
        return (evaluate(board), None)

    if maximizing:
        best = -math.inf
        move = None

        for action in board.moves():
            child = board.duplicate()
            child.make_move(action)
            new_depth = depth - 1
            (value, blank) = minimax(child, new_depth, False)
            if value > best:
                move = action
                best = value

        return (best, move)

    else:
        best = math.inf
        move = None

        for action in board.moves():
            child = board.duplicate()
            child.make_move(action)
            new_depth = depth - 1
            (value, blank) = minimax(child, new_depth, True)
            if value < best:
                move = action
                best = value

        return (best, move)

