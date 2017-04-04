INITAL_POSITION = 'pwa2 pwb2 pwc2 pwd2 pwe2 pwf2 pwg2 pwh2 '
INITAL_POSITION += 'pba7 pbb7 pbc7 pbd7 pbe7 pbf7 pbg7 pbh7 '
INITAL_POSITION += 'rwa1 nwb1 bwc1 qwd1 kwe1 bwf1 nwg1 rwh1 '
INITAL_POSITION += 'rba8 nbb8 bbc8 qbd8 kbe8 bbf8 nbg8 rbh8 '
COLUMNS = 'abcdefgh';
BOARD_SIZE = 8

import os
from pieces.make_piece import make_piece
from pieces.king import King
from pieces.pawn import Pawn
import utils as util
import cProfile


class Board:
    def __init__ (self, position=INITAL_POSITION, callback=lambda x: x):
        parts = position.split(',')
        self._turn = 'w' if len(parts) < 2 else parts[1].strip()
        piece_strings = parts[0].split()
        self._pieces = list(map(make_piece, piece_strings))
        self._last_move = None if len(parts) < 3 else parts[2].strip()
        self._history = []
        self._previous = None
        self._callback = callback

    def __str__ (self):
        rge = range(1, BOARD_SIZE + 1)
        pieceMap = {};

        # Pull out pieces into map first to make time complexity O(p + size ** 2)
        for piece in self._pieces:
            pieceMap[piece._square] = piece

        squares = pieceMap.keys()
        result = ''

        # Go through row first for printing to console
        for row in rge:
            for col in rge:
                if (col, row) in squares:
                    result += ' ' + pieceMap[(col, row)].__str__() + ' '
                else:
                    result += ' '

            if row != BOARD_SIZE:
                result += '\n\n'

        return result


    def serialize(self):
        string = [p.print() for p in self._pieces]
        last_move = '' if self._last_move == None else ', ' + self._last_move
        move = ', ' + self._turn
        return ' '.join(string) + move + last_move

    def turn(self):
        return self._turn

    def switch_turn(self):
        if self._turn == 'w':
            self._turn = 'b'
        elif self._turn == 'b':
            self._turn = 'w'
        else:
            raise ValueError('Unknown turn')

    def last(self, move, state):
        self._last_move = move
        self._history.append(move)
        self._previous = state

    def remove_piece(self, piece):
        self._pieces.remove(piece)

    def insert_piece(self, piece):
        self._pieces.append(piece)

    def move(self, move_string):
        move_string = str(move_string)
        parts = move_string.split()

        is_special = move_string == '0 0' or move_string == '0 0 0'

        if len(parts) > 3 or len(parts) < 2:
            raise ValueError('Invalid move input')
        elif not util.valid_square(parts[0]) and not is_special:
            raise ValueError('First square is not a valid square')
        elif not util.valid_square(parts[1]) and not is_special:
            raise ValueError('Second square is not a valid square')
        elif not is_special and not self.piece_on(parts[0]):
            raise ValueError('No piece on square')
        elif not is_special and self.piece_on(parts[0])._color != self.turn():
            raise ValueError('Cannot move opponents piece silly')
        elif not move_string in self.moves():
            raise ValueError('Illegal move.')
        else:
            self.make_move(move_string)
            if len(self.moves()) < 1:
                self._callback('Game Over')

    def make_move(self, move_string):
        """
            Makes a move without any validation and will not update the state
            of the board or any contents.

            Returns (capture, [moved_pieces])
        """


    def moves(self):
        """
            Returns a list of valid moves
        """
        deepArray = [piece.moves(self) for piece in self._pieces if piece._color == self._turn]
        return [item for sublist in deepArray for item in sublist]

    @staticmethod
    def moves_without_check_validation(board):
        pieces = board.get_pieces(lambda p: p._color == board.turn())
        move_mat = list(map(lambda p: p.moves(board), pieces))
        return [x for y in move_mat for x in y]


    def get_pieces(self, fn):
        return [x for x in self._pieces if fn(x)]

    def get_piece(self, fn):
        pieces = self.get_pieces(fn)
        if len(pieces) > 1:
            raise ValueError('More then one piece matched critera')

        if len(pieces) < 1:
            return None

        return pieces[0]

    def piece_on(self, square):
        return self.get_piece(lambda p: p._square == square)

    def undo(self):
        if self._previous:
            return Board(self._previous)
        else:
            return self

    def duplicate(self):
        state = self.serialize()
        return Board(state)

if __name__ == "__main__":
    board = Board('pwa2 pwb2 pwc2 pwd2 pwe2 pwf2 pwg2 pwh2 pba7 pbb7 pbc7 pbd7 pbe7 pbf7 pbg7 pbh7 ')
    print(board)
    # print(board.moves())

