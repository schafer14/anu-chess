import random
import sys
import os
import argparse

from board import Board
import randy

INITAL_POSITION = 'pwa2 pwb2 pwc2 pwd2 pwe2 pwf2 pwg2 pwh2 '
INITAL_POSITION += 'pba7 pbb7 pbc7 pbd7 pbe7 pbf7 pbg7 pbh7 '
INITAL_POSITION += 'rwa1 nwb1 bwc1 qwd1 kwe1 bwf1 nwg1 rwh1 '
INITAL_POSITION += 'rba8 nbb8 bbc8 qbd8 kbe8 bbf8 nbg8 rbh8 '

class Game():
    def __init__(self, player_1 = 'Challenger', player_2 = 'Random Randy',
                 player_1_type = 'human', player_2_type = 'bot', player_1_strategy = None,
                 player_2_strategy = randy, start = INITAL_POSITION):

        player_1 = {
            'agent_type': player_1_type,
            'name': player_1,
            'strategy': player_1_strategy
        }

        player_2 = {
            'agent_type': player_2_type,
            'name': player_2,
            'strategy': player_2_strategy,
        }

        self._continue = True
        self.players = dict()

        self.players['w'] = player_1
        self.players['b'] = player_2

        self.board = Board(start, self.game_over)

    def __str__(self):
        os.system('clear')
        return ('\n').join([
            "{} ({})".format(self.players['b']['name'], self.players['b']['agent_type']),
            self.board.__str__(),
            "{} ({})".format(self.players['w']['name'], self.players['w']['agent_type']),
        ])

    def game_over(self, result):
        self._continue = False

    def cli(self):
        print(self)
        # while self._continue:
        #     turn = self.board.turn()
        #     if self.players[turn]['agent_type'] != 'bot':
        #         move = input("Please enter a move: ")
        #         if move == 'q' or move == 'quit':
        #             break;
        #         elif move == 'p' or move == 'print':
        #             print(self.board.serialize())
        #         elif move == 'h' or move == 'help':
        #             print('Getting Moves')
        #             print(self.board.moves())
        #         elif move == 'u' or move == 'undo':
        #             self.board = self.board.undo()
        #             print(self.board)
        #         else:
        #             # try:
        #                 self.board.move(move)
        #                 print(self)
        #             # except:
        #             #     print('An error occured:', sys.exc_info()[1])
        #             #     print(sys.exc_info()[2])
        #     else:
        #         move = self.players[turn]['strategy'].move(self.board)
        #         try:
        #             self.board.move(move)
        #             print(self)
        #         except:
        #             print('An error occured:', sys.exc_info()[1])

        print('Game Over!')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chess or something')
    parser.add_argument('--ai', type=str, help='The location of the Ai module', default='../ai')
    parser.add_argument('--player1', type=str, help='The name of player 1', default='Challenger')
    parser.add_argument('--player2', type=str, help='The name of player 2', default='Random Randy')
    parser.add_argument('--start', type=str, help='Starting position', default=INITAL_POSITION)
    args = parser.parse_args()

    path = os.path.abspath(args.ai)
    sys.path.append(path)

    from ai import xavier

    game = Game(args.player1, args.player2, player_2_type='bot', player_2_strategy = xavier, start = args.start)
    game.cli()
