from .piece import Piece
from .rook import Rook
import utils as util

class King(Piece):
    def __init__(self, color, square, moved):
        super().__init__(color, square, 'k', moved)

    def __str__(self):
        return '♔' if self._color == 'b' else '♚'

    def moves(self, board):
        moves = []
        square = self._square
        (x, y) = util.square_to_mat(self._square)

        directions = [
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
        ]

        for (nx, ny) in directions:
            i = 1

            potential_move = (x + nx * i, y + ny * i)

            if util.valid_mat(potential_move):
                opp = board.piece_on(util.mat_to_square(potential_move))

                if not opp or not opp._color == self._color:
                    move = util.mat_to_square(potential_move)
                    moves.append('{} {}'.format(self._square, move))

        # Castling
        if self._has_moved == False:
            rook_right = board.piece_on('h{}'.format(square[1]))
            rook_left = board.piece_on('a{}'.format(square[1]))

            if (rook_right and rook_right._has_moved == False):
                if not(board.piece_on('f{}'.format(square[1])) or board.piece_on('g{}'.format(square[1]))):
                    moves.append('0 0')

            if (rook_left and rook_left._has_moved == False):
                if not(board.piece_on('b{}'.format(square[1])) or board.piece_on('c{}'.format(square[1])) or board.piece_on('d{}'.format(square[1]))):
                    moves.append('0 0 0')

        return moves
