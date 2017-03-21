from .piece import Piece
import engine.utils as util

class Knight(Piece):
    def __init__(self, color, square, moved):
        super().__init__(color, square, 'n', moved)

    def __str__(self):
        return '♘' if self._color == 'b' else '♞'

    def moves(self, board):
        moves = []
        (x, y) = util.square_to_mat(self._square)

        directions = [
            (x + 2, y + 1),
            (x + 2, y - 1),
            (x + 1, y + 2),
            (x + 1, y - 2),
            (x - 1, y + 2),
            (x - 1, y - 2),
            (x - 2, y + 1),
            (x - 2, y - 1),
        ]

        for move in directions:
            if util.valid_mat(move):
                square = util.mat_to_square(move)
                if (not board.piece_on(square) or board.piece_on(square)._color != self._color):
                    moves.append('{} {}'.format(self._square, square))

        return moves
