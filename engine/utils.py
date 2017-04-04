COLUMNS = 'abcdefgh';




def mat_to_square(mat):
    (x, y) = mat
    col = COLUMNS[x - 1]

    return '{}{}'.format(col, y)

def square_to_mat(square):
    col_name = square[0]
    col_index = COLUMNS.index(col_name) + 1

    row_index = int(square[1])

    return (col_index, row_index)

def valid_mat(mat):
    (x, y) = mat
    return x > 0 and x <= 8 and y > 0 and y <= 8

def expand_in_directions(board, square, directions, color):
    (x, y) = square_to_mat(square)
    moves = []

    for (nx, ny) in directions:
        i = 0
        while True:
            i += 1
            potential_move = (x + nx * i, y + ny * i)

            if not valid_mat(potential_move):
                break

            piece_on_new_square = board.piece_on(mat_to_square(potential_move))

            if piece_on_new_square and piece_on_new_square._color == color:
                break

            elif piece_on_new_square and not piece_on_new_square._color == color:
                move = mat_to_square(potential_move)
                moves.append('{} {}'.format(square, move))
                break

            else:
                move = mat_to_square(potential_move)
                moves.append('{} {}'.format(square, move))

    return moves
