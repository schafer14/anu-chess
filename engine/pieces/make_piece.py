from .pawn import Pawn
from .rook import Rook
from .bishop import Bishop
from .knight import Knight
from .queen import Queen
from .king import King

pieceMap = {
    'p': Pawn,
    'r': Rook,
    'n': Knight,
    'b': Bishop,
    'q': Queen,
    'k': King
};

def make_piece(piece):
    piece_type = piece[0]
    color = piece[1]
    square = piece[2:4]
    if len(piece) > 4:
        moved = True
    else:
        moved = False

    return pieceMap[piece_type](color, square, moved)

