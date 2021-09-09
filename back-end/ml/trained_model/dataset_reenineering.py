import os
import chess
import chess.pgn
import pandas as pd
import numpy as np

PLAYERS_FOLDER = './archive/Raw_game/Raw_game/'

def get_board_features(board):
    board_features = []
    for square in chess.SQUARES:
        # R N B K Q P r n b k q p
        piece = {'None': 0, 'R': 1, 'N': 2, 'B': 3, 'K': 4, 'Q': 5, 'P': 6, 'r': 7, 'n': 8, 'b': 9, 'k': 10, 'q': 11, 'p': 12}[str(board.piece_at(square))]
        board_features.append(piece)
    return board_features

def get_move_features(move):
    from_ = np.zeros(64)
    to_ = np.zeros(64)
    from_[move.from_square] = 1
    to_[move.to_square] = 1
    return from_, to_

def play(board, white_won, data, game_moves, nb_moves = 0):
    
    if(nb_moves == len(game_moves)):
        return
    else:
        if((white_won and board.turn) or (not white_won and not board.turn)):
            legal_moves = list(board.legal_moves)
            good_move = game_moves[nb_moves]
            bad_moves = list(filter(lambda x: x != good_move, legal_moves))

            board_features = get_board_features(board)
            line = np.array([], dtype = object) 
            #append bad moves to data
            for move in bad_moves:
                from_square, to_square = get_move_features(move)
                line = np.concatenate((board_features, from_square, to_square, list([False])))
                data.append(line)
            
            #append good move to data
            from_square, to_square = get_move_features(good_move)
            line = np.concatenate((board_features, from_square, to_square, list([True])))
            data.append(line)
        
        board.push(game_moves[nb_moves])
        return play(board, white_won, data, game_moves, nb_moves +1)
        


def rewrite_game(game_path, player):
    
    abs_path = os.path.abspath(game_path)
    pgn = open(abs_path)
    game = chess.pgn.read_game(pgn)

    result = {'1-0': True, '1/2-1/2': None, '0-1': False}[game.headers['Result']] 

    data = []

    if(result == None):
        return
    elif(result):
        white_won = True
    else:
        white_won = False

    game_moves = list(game.mainline_moves())
    board = game.board()

    play(board, white_won, data, game_moves)

    board_feature_names = chess.SQUARE_NAMES
    move_from_feature_names = ['from_' + square for square in chess.SQUARE_NAMES]
    move_to_feature_names = ['to_' + square for square in chess.SQUARE_NAMES]

    columns = board_feature_names + move_from_feature_names + move_to_feature_names + list(['good_move'])


    df = pd.DataFrame(data = data, columns = columns)

    print(player, df.shape)

    filename = './good_moves.csv'
    abs_filename = os.path.abspath(filename)

    df.to_csv(abs_filename, mode='a', index = False, header = not os.path.exists(abs_filename))

    return

def main():

    folders = list(os.walk(PLAYERS_FOLDER))
    players_folder = folders[0][1] # Getting players folders: ['Botvinnik', 'Caruana', 'Fischer', 'Anand', 'Alekhine', 'Tal', 'Polgar', 'Morphy', 'Carlsen', 'Capablanca', 'Nakamura', 'Kasparov']
    # for games_pgn in os.walk(PLAYERS_FOLDER + 'Capablanca'):
    #     for game in games_pgn[2]:
    #         rewrite_game(PLAYERS_FOLDER + 'Capablanca' + '/' + game, 'Capablanca')
    for player in players_folder[:int(len(players_folder) * 0.5)]:
        for games_pgn in os.walk(PLAYERS_FOLDER + player):
            for game in games_pgn[2]:
                rewrite_game(PLAYERS_FOLDER + player + '/' + game, player)

if __name__ == '__main__':
    main()
    