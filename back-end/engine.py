from stockfish import Stockfish
import chess
import chess.pgn
import io
import random
from sys import platform
import numpy as np

pawn_white_eval = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                            [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                            [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                            [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                            [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                            [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], np.float)

pawn_black_eval = pawn_white_eval[::-1]


knight_white_eval = np.array([[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                              [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                              [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                              [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                              [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                              [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
                              [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
                              [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]], np.float)

knight_black_eval = knight_white_eval[::-1]


bishop_white_eval = np.array([[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                              [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                              [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                              [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                              [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                              [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                              [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                              [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]], np.float)

bishop_black_eval = bishop_white_eval[::-1]


rook_white_eval = np.array([[0.0, 0.0, 0.0, 0.0, 0.0,  0.0, 0.0, 0.0],
                            [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                            [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]], np.float)

rook_black_eval = rook_white_eval[::-1]


queen_white_eval = np.array([[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                             [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                             [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                             [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                             [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                             [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                             [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
                             [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]], np.float)

queen_black_eval = queen_white_eval[::-1]


king_white_eval = np.array([[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                            [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                            [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                            [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                            [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]], np.float)

king_black_eval = king_white_eval[::-1]


class Engine:

    def __init__(self):
        self.stockfish = None
        if platform == 'linux' or platform == 'linux2':
            self.stockfish = Stockfish('./stockfish/stockfish_14_x64')
        elif platform == 'darwin':
            self.stockfish = Stockfish()

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

    def get_minimax_best_move(self, board):
        '''
            Get pure minimax (no ml pre-filtering) best move
        '''
        for move in board.legal_moves:
            if(self.can_checkmate(move, board)): # first we check if there is an istant checkmate
                return move

        moves_num = len(list(board.legal_moves))
   
        # When there are too much moves, depth is decreased to avoid extreme slow down
        if(moves_num > 30):
            return self.minimax_root(2, board, pure_minimax = True)
        elif(moves_num > 10 and moves_num <= 30):
            return self.minimax_root(3, board, pure_minimax = True)
        else:
            return self.minimax_root(4, board, pure_minimax = True)

    def square_to_coord(self, square):
        '''
            Get square coordinates (from 0 to 7 both for rows and columns) from square.
            Example: f3 -> (5, 2)
        '''
        return {0:(7,0), 1:(7,1), 2:(7,2), 3:(7,3), 4:(7,4), 5:(7,5), 6:(7,6), 7:(7,7),
          8:(6,0), 9:(6,1), 10:(6,2), 11:(6,3), 12:(6,4), 13:(6,5), 14:(6,6), 15:(6,7), 
          16:(5,0), 17:(5,1), 18:(5,2), 19:(5,3), 20:(5,4), 21:(5,5), 22:(5,6), 23:(5,7),
          24:(4,0), 25:(4,1), 26:(4,2), 27:(4,3), 28:(4,4), 29:(4,5), 30:(4,6), 31:(4,7),
          32:(3,0), 33:(3,1), 34:(3,2), 35:(3,3), 36:(3,4), 37:(3,5), 38:(3,6), 39:(3,7),
          40:(2,0), 41:(2,1), 42:(2,2), 43:(2,3), 44:(2,4), 45:(2,5), 46:(2,6), 47:(2,7),
          48:(1,0), 49:(1,1), 50:(1,2), 51:(1,3), 52:(1,4), 53:(1,5), 54:(1,6), 55:(1,7),
          56:(0,0), 57:(0,1), 58:(0,2), 59:(0,3), 60:(0,4), 61:(0,5), 62:(0,6), 63:(0,7)}[square]


    def get_piece_value(self, board, piece, square):
        '''
            Get the piece value, based on both its value and its position.
        '''
        x, y = self.square_to_coord(square)
  
        if board.turn == chess.WHITE:
            sign_white = -1
            sign_black = 1
        else:
            sign_white = 1
            sign_black = -1

        if(piece == 'None'):
            return 0
        elif(piece == 'P'):
            return sign_white * (10 + pawn_white_eval[x][y])
        elif(piece == 'N'):
            return sign_white * (30 + knight_white_eval[x][y])
        elif(piece == 'B'):
            return sign_white * (30 + bishop_white_eval[x][y])
        elif(piece == 'R'):
            return sign_white * (50 + rook_white_eval[x][y])
        elif(piece == 'Q'):
            return sign_white * (90 + queen_white_eval[x][y])
        elif(piece == 'K'):
            return sign_white * (900 + king_white_eval[x][y])
        elif(piece == 'p'):
            return sign_black * (10 + pawn_black_eval[x][y])
        elif(piece == 'n'):
            return sign_black * (30 + knight_black_eval[x][y])
        elif(piece == 'b'):
            return sign_black * (30 + bishop_black_eval[x][y])
        elif(piece == 'r'):
            return sign_black * (50 + rook_black_eval[x][y])
        elif(piece == 'q'):
            return sign_black * (90 + queen_black_eval[x][y])
        elif(piece == 'k'):
            return sign_black * (900 + king_black_eval[x][y])


    def evaluate_board(self, board):
        evaluation = 0
        for square in chess.SQUARES:
            piece = str(board.piece_at(square))
            evaluation = evaluation + self.get_piece_value(board, piece, square)
        return evaluation


    def minimax(self, depth, board, alpha, beta, pure_minimax, is_maximising_player):
  
        if(depth == 0):
            return - self.evaluate_board(board)
        elif(depth > 3):
            if pure_minimax:
                legal_moves = board.legal_moves
            else:
                # legal_moves = find_best_moves(board, model, 0.75)
                legal_moves = board.legal_moves # TODO questo va poi sostituito con sopra
        else:
            legal_moves = list(board.legal_moves)

        if(is_maximising_player):
            best_move = -9999
            for move in legal_moves:
                board.push(move)
                best_move = max(best_move, self.minimax(depth-1, board, alpha, beta, pure_minimax = pure_minimax, is_maximising_player = not is_maximising_player))
                board.pop()
                alpha = max(alpha, best_move)
                if(beta <= alpha):
                    return best_move
            return best_move
        else:
            best_move = 9999
            for move in legal_moves:
                board.push(move)
                best_move = min(best_move, self.minimax(depth-1, board, alpha, beta, pure_minimax = pure_minimax, is_maximising_player = not is_maximising_player))
                board.pop()
                beta = min(beta, best_move)
                if(beta <= alpha):
                    return best_move
            return best_move


    def minimax_root(self, depth, board, pure_minimax = False, is_maximising_player = True):
        # only search the top 50% moves
        if pure_minimax:
            legal_moves = board.legal_moves
        else:
            # legal_moves = find_best_moves(board, model) TODO
            legal_moves = board.legal_moves # questo va sostituito poi con quello sopra
        best_move = -9999
        best_move_found = None

        for move in legal_moves:
            board.push(move)
            value = self.minimax(depth - 1, board, -10000, 10000, True, not is_maximising_player)
            board.pop()
            if(value >= best_move):
                best_move = value
                best_move_found = move

        return best_move_found
    
    
