from stockfish import Stockfish
import chess
import chess.pgn
import io
import random
from sys import platform
import numpy as np
import pickle
from minimax.search import search
from ml.filter import filter_good_moves
import time


class Engine:

    def __init__(self):
        self.stockfish = None
        if platform == 'linux' or platform == 'linux2':
            self.stockfish = Stockfish('./stockfish/stockfish_14_x64')
        elif platform == 'darwin':
            self.stockfish = Stockfish()

        with open('./ml/trained_model/dumped_clf.pkl', 'rb') as fid:
            self.classifier = pickle.load(fid)

    def get_stockfish_best_move(self, board):
        self.stockfish.set_fen_position(board.fen())
        return self.stockfish.get_best_move()

    def get_random_move(self, board):
        legal_moves = [str(move) for move in board.legal_moves]
        return random.choice(legal_moves)

    def can_checkmate(self, move, board):
        fen = board.fen()
        future_board = chess.Board(fen)
        future_board.push(move)
        return future_board.is_checkmate()

    def get_minimax_best_move(self, board, with_ml):
        '''
            Get pure minimax (no ml pre-filtering) best move
        '''

        if board.turn == chess.WHITE:
            is_ai_white = True
        else:
            is_ai_white = False

        for move in board.legal_moves:
            if(self.can_checkmate(move, board)): # first we check if there is an istant checkmate
                return move

        # moves_num = len(list(board.legal_moves))

        evaluation = -999999
        best_move_found = None 

        # Cycling the legal moves, finds the best one
        start = time.time()

        if with_ml:
            moves = filter_good_moves(board=board, classifier=self.classifier, first_print=True)
            print(moves)
        else:
            moves = list(board.legal_moves)

        if len(moves) == 1: 
            return str(moves[0])

        for move in moves:
            board.push(move)
            value = search(depth=6 if len(moves) <= 5 and with_ml else 3, alpha=-999999, beta=999999, board=board, is_ai_white=is_ai_white, with_ml=with_ml, classifier=self.classifier)
            print(f'Minimax for move {str(move)}: {str(value)}')
            board.pop()
            if(value >= evaluation):
                evaluation = value
                best_move_found = move
        end = time.time()
        print(f"Best move found: {str(best_move_found)} in {end-start} seconds. \n")
        return best_move_found
    

        # # When there are too much moves, depth is decreased to avoid extreme slow down
        # if(moves_num > 30):
        #     return self.minimax_starting_point(depth = 3, board = board, is_ai_white = is_ai_white, pure_minimax = True) # more than two is too low, moves are not accurate though
        # elif(moves_num > 10 and moves_num <= 30):
        #     return self.minimax_starting_point(depth = 4, board = board, is_ai_white = is_ai_white, pure_minimax = True)
        # else:
        #     return self.minimax_starting_point(depth = 5, board = board, is_ai_white = is_ai_white, pure_minimax = True)
    
    def get_minimax_ml_best_move(self, board):
        

        if board.turn == chess.WHITE:
            is_ai_white = True
        else:
            is_ai_white = False

        for move in board.legal_moves:
            if(self.can_checkmate(move, board)): # first we check if there is an istant checkmate
                return move
        
        


    # def get_board_features(self, board):
    #     board_features = []
    #     for square in chess.SQUARES:
    #         # R N B K Q P r n b k q p
    #         piece = {'None': 0, 'R': 1, 'N': 2, 'B': 3, 'K': 4, 'Q': 5, 'P': 6, 'r': 7, 'n': 8, 'b': 9, 'k': 10, 'q': 11, 'p': 12}[str(board.piece_at(square))]
    #         board_features.append(piece)
        
    #     return board_features

    # def get_move_features(self, move):
    #     from_ = np.zeros(64)
    #     to_ = np.zeros(64)
    #     from_[move.from_square] = 1
    #     to_[move.to_square] = 1
    #     return from_, to_

    # def filter_good_moves(self, board, proportion = 0.75):

    #     moves = []
    #     good_moves = []
    #     for move in list(board.legal_moves):
    #         board_features = self.get_board_features(board)
    #         from_square, to_square = self.get_move_features(move)
    #         line = np.concatenate((board_features, from_square, to_square))

    #         move_translated = np.array(["%.1f" % number for number in line])
    #         good_move_prob = self.classifier.predict_proba(move_translated.astype(np.float64).reshape(1, -1))[0][1]
    #         if good_move_prob > 0.4:
    #             good_moves.append([move, good_move_prob])
    #         moves.append([move, good_move_prob])
    #         #print(move, self.classifier.predict(move_translated.reshape(1, -1)), self.classifier.predict_proba(move_translated.reshape(1, -1)))
    #     moves = sorted(moves, key=lambda k: k[1], reverse = True) 

    #     if len(good_moves) == 0:
    #         print("No good moves found")
    #         for move in moves[:int(len(moves) * 0.25)]:
    #             print(f'Move: {str(move[0])} | Prob: {move[1]}')

    #         moves = [move[0] for move in moves]
    #         return moves[:int(len(moves) * 0.25)]

    #     print(f"{len(good_moves)} good moves found")
    #     for move in good_moves:
    #             print(f'Move: {str(move[0])} | Prob: {move[1]}')

    #     good_moves = [move[0] for move in good_moves]
    #     return good_moves[:int(len(good_moves) * 0.25)]

    # def minimax_starting_point(self, depth, board, is_ai_white, pure_minimax = False, is_maximising_player = True):
    #     '''
    #         Starting point for minimax algorithm, the best move is returned.
    #         This function is used both for pure minimax and minimax&MachineLearning
    #     '''
        
    #     moves_num = len(list(board.legal_moves))
    #     if pure_minimax:
    #         legal_moves = list(board.legal_moves)
    #     else:
    #         legal_moves = self.filter_good_moves(board)
    #         if(len(legal_moves) == 0):
    #             legal_moves = list(board.legal_moves)

    #     evaluation = -999999
    #     best_move_found = None
    #     print(f"Filtered good moves {len(legal_moves)}/{moves_num}: ")
        
    #     if len(legal_moves) == 1:
    #         return legal_moves[0]

    #     # Cycling the legal moves, finds the best one
    #     for move in legal_moves:
    #         board.push(move)
    #         value = self.minimax(depth = depth - 1, 
    #                             board = board, 
    #                             is_ai_white = is_ai_white , 
    #                             alpha = -10000, 
    #                             beta = 10000, 
    #                             pure_minimax = True, 
    #                             is_maximising_player = not is_maximising_player)
    #         print(f'Minimax (depth: {depth}) for move {str(move)}: {str(value)}')
    #         board.pop()
    #         if(value >= evaluation):
    #             evaluation = value
    #             best_move_found = move

    #     print(f"Best move found: {str(best_move_found)}\n")
    #     return best_move_found
    
    # def minimax(self, depth, board, is_ai_white, alpha, beta, pure_minimax, is_maximising_player):
        
    #     '''
    #         Get the evaluation for a specific move. This is recursive.
    #     '''

    #     if(depth == 0):
    #         # When minimax reaches depth 0, it returns the evaluation of the move.
    #         return - self.evaluate_board(board, is_ai_white)
    #     else:
    #         if pure_minimax:
    #             legal_moves = list(board.legal_moves)
    #         else:
    #             legal_moves = self.filter_good_moves(board)

    #     if(is_maximising_player):
    #         best_move = -9999
    #         for move in legal_moves:
    #             board.push(move)
    #             best_move = max(best_move, self.minimax(depth = depth-1, 
    #                                                     board = board, 
    #                                                     is_ai_white = is_ai_white, 
    #                                                     alpha = alpha, 
    #                                                     beta = beta, 
    #                                                     pure_minimax = pure_minimax, 
    #                                                     is_maximising_player = not is_maximising_player))
    #             board.pop()
    #             alpha = max(alpha, best_move)
    #             if(beta <= alpha):
    #                 return best_move
    #         return best_move
    #     else:
    #         best_move = 9999
    #         for move in legal_moves:
    #             board.push(move)
    #             best_move = min(best_move, self.minimax(depth = depth-1, 
    #                                                     board = board, 
    #                                                     is_ai_white = is_ai_white, 
    #                                                     alpha = alpha, 
    #                                                     beta = beta, 
    #                                                     pure_minimax = pure_minimax, 
    #                                                     is_maximising_player = not is_maximising_player))
    #             board.pop()
    #             beta = min(beta, best_move)
    #             if(beta <= alpha):
    #                 return best_move
    #         return best_move

    # def evaluate_board(self, board, is_ai_white):
    #     '''
    #         Get the evaluation for a specific board setup.
    #         This is based on the pieces value their positions.
    #     '''
    #     evaluation = 0

    #     for square in chess.SQUARES:
    #         piece = str(board.piece_at(square))
    #         evaluation = evaluation + self.get_piece_value(board, is_ai_white, piece, square)

    #     return evaluation

    # def get_piece_value(self, board, is_ai_white, piece, square):
    #     '''
    #         Get the piece value, based on both its value and its position.
    #     '''
    #     x, y = self.square_to_coord(square)
  
    #     if is_ai_white:
    #         sign_white = -1
    #         sign_black = 1
    #     else:
    #         sign_white = 1
    #         sign_black = -1

    #     if(piece == 'None'):
    #         return 0
    #     elif(piece == 'P'):
    #         return sign_white * (10 + pawn_white_eval[x][y])
    #     elif(piece == 'N'):
    #         return sign_white * (30 + knight_white_eval[x][y])
    #     elif(piece == 'B'):
    #         return sign_white * (30 + bishop_white_eval[x][y])
    #     elif(piece == 'R'):
    #         return sign_white * (50 + rook_white_eval[x][y])
    #     elif(piece == 'Q'):
    #         return sign_white * (90 + queen_white_eval[x][y])
    #     elif(piece == 'K'):
    #         return sign_white * (900 + king_white_eval[x][y])
    #     elif(piece == 'p'):
    #         return sign_black * (10 + pawn_black_eval[x][y])
    #     elif(piece == 'n'):
    #         return sign_black * (30 + knight_black_eval[x][y])
    #     elif(piece == 'b'):
    #         return sign_black * (30 + bishop_black_eval[x][y])
    #     elif(piece == 'r'):
    #         return sign_black * (50 + rook_black_eval[x][y])
    #     elif(piece == 'q'):
    #         return sign_black * (90 + queen_black_eval[x][y])
    #     elif(piece == 'k'):
    #         return sign_black * (900 + king_black_eval[x][y])

    # def square_to_coord(self, square):
    #     '''
    #         Get square coordinates (from 0 to 7 both for rows and columns) from square.
    #         Example: f3 -> (5, 2)
    #     '''
    #     return {0:(7,0), 1:(7,1), 2:(7,2), 3:(7,3), 4:(7,4), 5:(7,5), 6:(7,6), 7:(7,7),
    #       8:(6,0), 9:(6,1), 10:(6,2), 11:(6,3), 12:(6,4), 13:(6,5), 14:(6,6), 15:(6,7), 
    #       16:(5,0), 17:(5,1), 18:(5,2), 19:(5,3), 20:(5,4), 21:(5,5), 22:(5,6), 23:(5,7),
    #       24:(4,0), 25:(4,1), 26:(4,2), 27:(4,3), 28:(4,4), 29:(4,5), 30:(4,6), 31:(4,7),
    #       32:(3,0), 33:(3,1), 34:(3,2), 35:(3,3), 36:(3,4), 37:(3,5), 38:(3,6), 39:(3,7),
    #       40:(2,0), 41:(2,1), 42:(2,2), 43:(2,3), 44:(2,4), 45:(2,5), 46:(2,6), 47:(2,7),
    #       48:(1,0), 49:(1,1), 50:(1,2), 51:(1,3), 52:(1,4), 53:(1,5), 54:(1,6), 55:(1,7),
    #       56:(0,0), 57:(0,1), 58:(0,2), 59:(0,3), 60:(0,4), 61:(0,5), 62:(0,6), 63:(0,7)}[square]