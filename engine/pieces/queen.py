from .piece import Piece
import engine.utils as util

class Queen(Piece):
    def __init__(self, color, square, moved):
        super().__init__(color, square, 'q', moved)

    def __str__(self):
        return '♕' if self._color == 'b' else '♛'

    def moves(self, board):
        moves = []

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

        return util.expand_in_directions(board, self._square, directions, self._color)

