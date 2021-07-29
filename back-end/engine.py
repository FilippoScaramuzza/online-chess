from stockfish import Stockfish
import chess
import chess.pgn
import io
import random
from sys import platform

class Engine:

    def __init__(self, board):
        self.board = board

    def get_stockfish_best_move(self):
        stockfish = None
        if platform == 'linux' or platform == 'linux2':
            stockfish = Stockfish('./stockfish/stockfish_14_x64')
        elif platform == 'darwin':
            stockfish = Stockfish()    
        stockfish.set_fen_position(self.board.fen())
        return stockfish.get_best_move()

    def get_random_move(self):
        legal_moves = [str(move) for move in board.legal_moves]
        return random.choice(legal_moves)
    