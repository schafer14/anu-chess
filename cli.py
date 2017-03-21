import engine
import sys

# board = engine.Board()
board = engine.Board('pwa2 pwb2 pwc2 pwd5m pwe2 pwf2 pwg2 pwh2 pba7 pbb7 pbc5m pbd6m pbe7 pbf7 pbg7 pbh7 rwa1 nwb1 bwc1 qwd1 kwe1 bwf1 nwg1 rwh1 rba8 nbb8 bbc8 qbd8 kbe8 bbf8 nbg8 rbh8, w, c7 c5')

print(board);

while True:
    move = input("Please enter a move for {}: ".format(board.turn()))
    if move == 'q' or move == 'quit':
        break;
    elif move == 'p' or move == 'print':
        print(board.serialize())
    elif move == 'h' or move == 'help':
        print('Getting Moves')
        print(engine.generator.moves(board))
    elif move == 'u' or move == 'undo':
        board = board.undo()
        print(board)
    else:
        try:
            board.move(move)
            print(board)
        except:
            print('An error occured:', sys.exc_info()[1])

