import utils as util

COLUMNS = 'abcdefgh'

class Piece():
    def __init__(self, color, square, symbol, has_moved = False):
        self._has_moved = has_moved
        self._color = color
        self._square = util.square_to_mat(square)
        self._symbol = symbol

    def __str__(self):
        return 'X'

    def print(self):
        moved = 'm' if self._has_moved else ''
        return '{}{}{}{}'.format(self._symbol, self._color, util.mat_to_square(self._square), moved)

    def moves(self, board):
        return [];

    def on_row(self, row):
        return int(self._square[1]) == row

    def on_column(self, col):
        return self._square[0] == col

    def on_square(self, square):
        return self._square == square

    def move(self, square):
        # print('Moving {} {} -> {}'.format(self, self._square, square))
        self._square = square
        self._has_moved = True
