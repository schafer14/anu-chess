import engine.utils as util
from engine.pieces.king import King

def moves(main_board):
    pieces = main_board.get_pieces(lambda p: p._color == main_board.turn())
    move_mat = list(map(lambda p: p.moves(main_board), pieces))
    moves = [x for y in move_mat for x in y]

    # Make the move; Check if the move is moving the king into check; undo move
    removeables = []
    for move in moves:
        cloned_board = main_board.duplicate()
        cloned_board.make_move(move)
        cloned_king = main_board.get_piece(lambda p: p._color == main_board.turn() and isinstance(p, King))

        king_square = cloned_king._square
        king_row = king_square[1]

        for opp_move_str in moves_without_check_validation(cloned_board):
            opp_move = opp_move_str.split()
            if opp_move[1] == king_square and move in moves:
                print(move, opp_move)
                removeables.append(move)
                break

            # Cannot castle through check or from check
            if move == '0 0':
                if opp_move[1] == 'e{}'.format(king_row) or opp_move[1] == 'f{}'.format(king_row):
                    removeables.append(move)
                    break

            if move == '0 0 0':
                if opp_move[1] == 'e{}'.format(king_row) or opp_move[1] == 'd{}'.format(king_row) or opp_move[1] == 'c{}'.format(king_row):
                    removeables.append(move)
                    break

    for move in removeables:
        moves.remove(move)

    return moves

def moves_without_check_validation(board):
    pieces = board.get_pieces(lambda p: p._color == board.turn())
    move_mat = list(map(lambda p: p.moves(board), pieces))
    return [x for y in move_mat for x in y]
