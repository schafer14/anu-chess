from .piece import Piece
import engine.utils as util

class Pawn(Piece):
    def __init__(self, color, square, moved):
        super().__init__(color, square, 'p', moved)

    def __str__(self):
        return '♙' if self._color == 'b' else '♟'

    def moves(self, board):
        (x, y) = util.square_to_mat(self._square)
        direction = 1 if self._color == 'w' else -1
        moves = []

        # Straights
        straight_1 = util.mat_to_square((x, y + (direction)))
        straight_2 = util.mat_to_square((x, y + (2 * direction)))

        if (board.piece_on(straight_1) == None and util.valid_square(straight_1)):
            moves.append(straight_1)

        if (board.piece_on(straight_2) == None and self._has_moved == False and util.valid_square(straight_2)):
            moves.append(straight_2)

        # Captures
        capture_1 = (x + 1, y + direction)
        capture_2 = (x - 1, y + direction)

        if (util.valid_mat(capture_1)):
            square = util.mat_to_square(capture_1)
            if (board.piece_on(square)
                and board.piece_on(square) != self._color):
                    moves.append(square)

        if (util.valid_mat(capture_2)):
            square = util.mat_to_square(capture_2)
            if (board.piece_on(square)
                and board.piece_on(square) != self._color):
                    moves.append(square)


        # En passent
        en_passent_1 = (x + 1, y)
        en_passent_2 = (x - 1, y)

        if (util.valid_mat(en_passent_1) and board._last_move):
            square = util.mat_to_square(en_passent_1)
            result_square = util.mat_to_square((x + 1, y + direction))
            last_move = board._last_move.split()
            if (last_move[1] == square):
                opponent = board.piece_on(square)
                if (isinstance(opponent, Pawn)):
                    if (abs(int(last_move[0][1]) - int(last_move[1][1])) == 2):
                        moves.append(result_square)

        if (util.valid_mat(en_passent_2) and board._last_move):
            square = util.mat_to_square(en_passent_2)
            result_square = util.mat_to_square((x - 1, y + direction))
            last_move = board._last_move.split()
            if (last_move[1] == square):
                opponent = board.piece_on(square)
                if (isinstance(opponent, Pawn)):
                    if (abs(int(last_move[0][1]) - int(last_move[1][1])) == 2):
                        moves.append(result_square)

        full_moves = list(map(lambda m: '{} {}'.format(self._square, m), moves))

        # Promotion
        promotion_squares = []
        for move in full_moves:
            parts = move.split()
            if int(parts[1][1]) == 0 or int(parts[1][1]) == 8:
                full_moves.remove(move)
                promotion_squares.append(move)

        for move in promotion_squares:
            full_moves.append(move + ' q')
            full_moves.append(move + ' r')
            full_moves.append(move + ' b')
            full_moves.append(move + ' n')

        return full_moves

