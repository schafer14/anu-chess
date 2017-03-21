INITAL_POSITION = 'pwa2 pwb2 pwc2 pwd2 pwe2 pwf2 pwg2 pwh2 '
INITAL_POSITION += 'pba7 pbb7 pbc7 pbd7 pbe7 pbf7 pbg7 pbh7 '
INITAL_POSITION += 'rwa1 nwb1 bwc1 qwd1 kwe1 bwf1 nwg1 rwh1 '
INITAL_POSITION += 'rba8 nbb8 bbc8 qbd8 kbe8 bbf8 nbg8 rbh8 '
COLUMNS = 'abcdefgh';
BOARD_SIZE = 8

import os
from engine.pieces.make_piece import make_piece
from engine.pieces.king import King
from engine.pieces.pawn import Pawn
import engine.utils as util
import engine.move_generator as generator


class Board:
    def __init__ (self, position=INITAL_POSITION):
        parts = position.split(',')
        self._turn = 'w' if len(parts) < 2 else parts[1].strip()
        piece_strings = parts[0].split()
        self._pieces = list(map(make_piece, piece_strings))
        self._last_move = None if len(parts) < 3 else parts[2].strip()
        self._history = []
        self._previous = None

    def __str__ (self):
        def displayRow(rowNumber):
            row = BOARD_SIZE-rowNumber
            pieces = list(filter(lambda p: p.on_row(row), self._pieces))

            def displayCell(column):
                piece = list(filter(lambda p: p.on_column(column), pieces))
                return ' ' if len(piece) == 0 else piece[0].__str__()

            mat = list(map(displayCell, COLUMNS))
            return ' | '.join(mat)

        os.system('clear')
        mat = list(map(displayRow, range(BOARD_SIZE)))
        return '\n\n'.join(mat)

    def serialize(self):
        string = list(map(lambda p: p.print(), self._pieces))
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
        elif not is_special and not self.piece_on(parts[0])._color:
            raise ValueError('No piece on square')
        elif not is_special and self.piece_on(parts[0])._color != self.turn():
            raise ValueError('Cannot move opponents piece silly')
        elif not move_string in generator.moves(self):
            raise ValueError('Illegal move.')
        else:
            self.make_move(move_string)

    def make_move(self, move_string):
        """
            Makes a move without any validation and will not update the state
            of the board or any contents.

            Returns (capture, [moved_pieces])
        """
        state = self.serialize()
        move = move_string.split()
        king_row = 1 if self.turn() == 'w' else BOARD_SIZE

        # First check castling because it's a little special
        if move_string == '0 0':
            king = self.piece_on('e{}'.format(king_row))
            rook = self.piece_on('h{}'.format(king_row))

            king.move('g{}'.format(king_row))
            rook.move('f{}'.format(king_row))

        # Castling Queen Side
        elif move_string == '0 0 0':
            king = self.piece_on('e{}'.format(king_row))
            rook = self.piece_on('a{}'.format(king_row))

            king.move('c{}'.format(king_row))
            rook.move('d{}'.format(king_row))

        # Any other move will actually use the squares specified in the move_stirng
        else:
            piece = self.piece_on(move[0])
            old_piece = self.piece_on(move[1])

            if old_piece:
                self.remove_piece(old_piece)

            # Check for en passent
            if isinstance(piece, Pawn) and move[0][0] != move[1][0] and not old_piece:
                direction = 1 if self.turn() == 'w' else -1
                taken_square = (move[1][0]) + str(int(move[1][1]) - direction)
                old_piece = self.piece_on(taken_square)
                self.remove_piece(old_piece)

            # Check to see if the piece was promoted
            if len(move) > 2:
                self.pieces.remove(piece)
                new_piece = make_piece('{}{}{}'.format(move[2], self.turn, move[1]))
                self.pieces.append(new_piece)

            piece.move(move[1])
        self.switch_turn()
        self.last(move_string, state)

    def get_pieces(self, fn):
        return list(filter(fn, self._pieces))

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
