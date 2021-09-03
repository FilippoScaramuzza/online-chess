import chess
import numpy as np

pawn_white_eval = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 50, 9: 50, 10: 50, 11: 50, 12: 50, 13: 50, 14: 50, 15: 50, 16: 10, 17: 10, 18: 20, 19: 30, 20: 30, 21: 20, 22: 10, 23: 10, 24: 5, 25: 5, 26: 10, 27: 25, 28: 25, 29: 10, 30: 5,
    31: 5, 32: 0, 33: 0, 34: 0, 35: 20, 36: 20, 37: 0, 38: 0, 39: 0, 40: 5, 41: -5, 42: -10, 43: 0, 44: 0, 45: -10, 46: -5, 47: 5, 48: 5, 49: 10, 50: 10, 51: -20, 52: -20, 53: 10, 54: 10, 55: 5, 56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0}
pawn_black_eval = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 5, 9: 10, 10: 10, 11: -20, 12: -20, 13: 10, 14: 10, 15: 5, 16: 5, 17: -5, 18: -10, 19: 0, 20: 0, 21: -10, 22: -5, 23: 5, 24: 0, 25: 0, 26: 0, 27: 20, 28: 20, 29: 0, 30: 0, 31: 0,
    32: 5, 33: 5, 34: 10, 35: 25, 36: 25, 37: 10, 38: 5, 39: 5, 40: 10, 41: 10, 42: 20, 43: 30, 44: 30, 45: 20, 46: 10, 47: 10, 48: 50, 49: 50, 50: 50, 51: 50, 52: 50, 53: 50, 54: 50, 55: 50, 56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0}

knight_white_eval = {0: -50, 1: -40, 2: -30, 3: -30, 4: -30, 5: -30, 6: -40, 7: -50, 8: -40, 9: -20, 10: 0, 11: 0, 12: 0, 13: 0, 14: -20, 15: -40, 16: -30, 17: 0, 18: 10, 19: 15, 20: 15, 21: 10, 22: 0, 23: -30, 24: -30, 25: 5, 26: 15, 27: 20, 28: 20, 29: 15, 30: 5, 31: -
    30, 32: -30, 33: 0, 34: 15, 35: 20, 36: 20, 37: 15, 38: 0, 39: -30, 40: -30, 41: 5, 42: 10, 43: 15, 44: 15, 45: 10, 46: 5, 47: -30, 48: -40, 49: -20, 50: 0, 51: 5, 52: 5, 53: 0, 54: -20, 55: -40, 56: -50, 57: -40, 58: -30, 59: -30, 60: -30, 61: -30, 62: -40, 63: -50}
knight_black_eval = {0: -50, 1: -40, 2: -30, 3: -30, 4: -30, 5: -30, 6: -40, 7: -50, 8: -40, 9: -20, 10: 0, 11: 5, 12: 5, 13: 0, 14: -20, 15: -40, 16: -30, 17: 5, 18: 10, 19: 15, 20: 15, 21: 10, 22: 5, 23: -30, 24: -30, 25: 0, 26: 15, 27: 20, 28: 20, 29: 15, 30: 0, 31: -
    30, 32: -30, 33: 5, 34: 15, 35: 20, 36: 20, 37: 15, 38: 5, 39: -30, 40: -30, 41: 0, 42: 10, 43: 15, 44: 15, 45: 10, 46: 0, 47: -30, 48: -40, 49: -20, 50: 0, 51: 0, 52: 0, 53: 0, 54: -20, 55: -40, 56: -50, 57: -40, 58: -30, 59: -30, 60: -30, 61: -30, 62: -40, 63: -50}

bishop_white_eval = {0: -20, 1: -10, 2: -10, 3: -10, 4: -10, 5: -10, 6: -10, 7: -20, 8: -10, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: -10, 16: -10, 17: 0, 18: 5, 19: 10, 20: 10, 21: 5, 22: 0, 23: -10, 24: -10, 25: 5, 26: 5, 27: 10, 28: 10, 29: 5, 30: 5, 31: -
    10, 32: -10, 33: 0, 34: 10, 35: 10, 36: 10, 37: 10, 38: 0, 39: -10, 40: -10, 41: 10, 42: 10, 43: 10, 44: 10, 45: 10, 46: 10, 47: -10, 48: -10, 49: 5, 50: 0, 51: 0, 52: 0, 53: 0, 54: 5, 55: -10, 56: -20, 57: -10, 58: -10, 59: -10, 60: -10, 61: -10, 62: -10, 63: -20}
bishop_black_eval = {0: -20, 1: -10, 2: -10, 3: -10, 4: -10, 5: -10, 6: -10, 7: -20, 8: -10, 9: 5, 10: 0, 11: 0, 12: 0, 13: 0, 14: 5, 15: -10, 16: -10, 17: 10, 18: 10, 19: 10, 20: 10, 21: 10, 22: 10, 23: -10, 24: -10, 25: 0, 26: 10, 27: 10, 28: 10, 29: 10, 30: 0,
    31: -10, 32: -10, 33: 5, 34: 5, 35: 10, 36: 10, 37: 5, 38: 5, 39: -10, 40: -10, 41: 0, 42: 5, 43: 10, 44: 10, 45: 5, 46: 0, 47: -10, 48: -10, 49: 0, 50: 0, 51: 0, 52: 0, 53: 0, 54: 0, 55: -10, 56: -20, 57: -10, 58: -10, 59: -10, 60: -10, 61: -10, 62: -10, 63: -20}

rook_white_eval = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 5, 9: 10, 10: 10, 11: 10, 12: 10, 13: 10, 14: 10, 15: 5, 16: -5, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: -5, 24: -5, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0,
    31: -5, 32: -5, 33: 0, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0, 39: -5, 40: -5, 41: 0, 42: 0, 43: 0, 44: 0, 45: 0, 46: 0, 47: -5, 48: -5, 49: 0, 50: 0, 51: 0, 52: 0, 53: 0, 54: 0, 55: -5, 56: 0, 57: 0, 58: 0, 59: 5, 60: 5, 61: 0, 62: 0, 63: 0}
rook_black_eval = {0: 0, 1: 0, 2: 0, 3: 5, 4: 5, 5: 0, 6: 0, 7: 0, 8: -5, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: -5, 16: -5, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: -5, 24: -5, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0, 31: -5,
    32: -5, 33: 0, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0, 39: -5, 40: -5, 41: 0, 42: 0, 43: 0, 44: 0, 45: 0, 46: 0, 47: -5, 48: 5, 49: 10, 50: 10, 51: 10, 52: 10, 53: 10, 54: 10, 55: 5, 56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0}


queen_white_eval = {0: -20, 1: -10, 2: -10, 3: -5, 4: -5, 5: -10, 6: -10, 7: -20, 8: -10, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: -10, 16: -10, 17: 0, 18: 5, 19: 5, 20: 5, 21: 5, 22: 0, 23: -10, 24: -5, 25: 0, 26: 5, 27: 5, 28: 5, 29: 5, 30: 0,
    31: -5, 32: 0, 33: 0, 34: 5, 35: 5, 36: 5, 37: 5, 38: 0, 39: -5, 40: -10, 41: 5, 42: 5, 43: 5, 44: 5, 45: 5, 46: 0, 47: -10, 48: -10, 49: 0, 50: 5, 51: 0, 52: 0, 53: 0, 54: 0, 55: -10, 56: -20, 57: -10, 58: -10, 59: -5, 60: -5, 61: -10, 62: -10, 63: -20}
queen_black_eval = {0: -20, 1: -10, 2: -10, 3: -5, 4: -5, 5: -10, 6: -10, 7: -20, 8: -10, 9: 0, 10: 0, 11: 0, 12: 0, 13: 5, 14: 0, 15: -10, 16: -10, 17: 0, 18: 5, 19: 5, 20: 5, 21: 5, 22: 5, 23: -10, 24: -5, 25: 0, 26: 5, 27: 5, 28: 5, 29: 5, 30: 0,
    31: 0, 32: -5, 33: 0, 34: 5, 35: 5, 36: 5, 37: 5, 38: 0, 39: -5, 40: -10, 41: 0, 42: 5, 43: 5, 44: 5, 45: 5, 46: 0, 47: -10, 48: -10, 49: 0, 50: 0, 51: 0, 52: 0, 53: 0, 54: 0, 55: -10, 56: -20, 57: -10, 58: -10, 59: -5, 60: -5, 61: -10, 62: -10, 63: -20}

king_white_eval = {0: -30, 1: -40, 2: -40, 3: -50, 4: -50, 5: -40, 6: -40, 7: -30, 8: -30, 9: -40, 10: -40, 11: -50, 12: -50, 13: -40, 14: -40, 15: -30, 16: -30, 17: -40, 18: -40, 19: -50, 20: -50, 21: -40, 22: -40, 23: -30, 24: -30, 25: -40, 26: -40, 27: -50, 28: -50, 29: -40,
    30: -40, 31: -30, 32: -20, 33: -30, 34: -30, 35: -40, 36: -40, 37: -30, 38: -30, 39: -20, 40: -10, 41: -20, 42: -20, 43: -20, 44: -20, 45: -20, 46: -20, 47: -10, 48: 20, 49: 20, 50: 0, 51: 0, 52: 0, 53: 0, 54: 20, 55: 20, 56: 20, 57: 30, 58: 10, 59: 0, 60: 0, 61: 10, 62: 30, 63: 20}
king_black_eval = {0: 20, 1: 30, 2: 10, 3: 0, 4: 0, 5: 10, 6: 30, 7: 20, 8: 20, 9: 20, 10: 0, 11: 0, 12: 0, 13: 0, 14: 20, 15: 20, 16: -10, 17: -20, 18: -20, 19: -20, 20: -20, 21: -20, 22: -20, 23: -10, 24: -20, 25: -30, 26: -30, 27: -40, 28: -40, 29: -30, 30: -30, 31: -20, 32: -
    30, 33: -40, 34: -40, 35: -50, 36: -50, 37: -40, 38: -40, 39: -30, 40: -30, 41: -40, 42: -40, 43: -50, 44: -50, 45: -40, 46: -40, 47: -30, 48: -30, 49: -40, 50: -40, 51: -50, 52: -50, 53: -40, 54: -40, 55: -30, 56: -30, 57: -40, 58: -40, 59: -50, 60: -50, 61: -40, 62: -40, 63: -30}


def evaluate(board, is_ai_white):
    '''
        Get the evaluation for a specific board setup.
        This is based on the pieces value their positions.
    '''
    evaluation = 0

    for square in chess.SQUARES:
        piece = str(board.piece_at(square))
        evaluation = evaluation + \
            evaluate_position(board, is_ai_white, piece, square)

    return evaluation


def evaluate_position(board, is_ai_white, piece, square):
    '''
        Get the piece value, based on both its value and its position.
    '''

    if is_ai_white:
        sign_white = -1
        sign_black = 1
    else:
        sign_white = 1
        sign_black = -1

    if(piece == 'None'):
        return 0
    elif(piece == 'P'):
        return sign_white * (100 + pawn_white_eval[square])
    elif(piece == 'N'):
        return sign_white * (320 + knight_white_eval[square])
    elif(piece == 'B'):
        return sign_white * (330 + bishop_white_eval[square])
    elif(piece == 'R'):
        return sign_white * (500 + rook_white_eval[square])
    elif(piece == 'Q'):
        return sign_white * (900 + queen_white_eval[square])
    elif(piece == 'K'):
        return sign_white * (20000 + king_white_eval[square])
    elif(piece == 'p'):
        return sign_black * (100 + pawn_black_eval[square])
    elif(piece == 'n'):
        return sign_black * (320 + knight_black_eval[square])
    elif(piece == 'b'):
        return sign_black * (330 + bishop_black_eval[square])
    elif(piece == 'r'):
        return sign_black * (500 + rook_black_eval[square])
    elif(piece == 'q'):
        return sign_black * (900 + queen_black_eval[square])
    elif(piece == 'k'):
        return sign_black * (20000 + king_black_eval[square])


# def square_to_coord(square):
#     '''
#         Get square coordinates (from 0 to 7 both for rows and columns) from square.
#         Example: f3 -> (5, 2)
#     '''
#     return {0: (7, 0), 1: (7, 1), 2: (7, 2), 3: (7, 3), 4: (7, 4), 5: (7, 5), 6: (7, 6), 7: (7, 7),
#             8: (6, 0), 9: (6, 1), 10: (6, 2), 11: (6, 3), 12: (6, 4), 13: (6, 5), 14: (6, 6), 15: (6, 7),
#             16: (5, 0), 17: (5, 1), 18: (5, 2), 19: (5, 3), 20: (5, 4), 21: (5, 5), 22: (5, 6), 23: (5, 7),
#             24: (4, 0), 25: (4, 1), 26: (4, 2), 27: (4, 3), 28: (4, 4), 29: (4, 5), 30: (4, 6), 31: (4, 7),
#             32: (3, 0), 33: (3, 1), 34: (3, 2), 35: (3, 3), 36: (3, 4), 37: (3, 5), 38: (3, 6), 39: (3, 7),
#             40: (2, 0), 41: (2, 1), 42: (2, 2), 43: (2, 3), 44: (2, 4), 45: (2, 5), 46: (2, 6), 47: (2, 7),
#             48: (1, 0), 49: (1, 1), 50: (1, 2), 51: (1, 3), 52: (1, 4), 53: (1, 5), 54: (1, 6), 55: (1, 7),
#             56: (0, 0), 57: (0, 1), 58: (0, 2), 59: (0, 3), 60: (0, 4), 61: (0, 5), 62: (0, 6), 63: (0, 7)}[square]


# pawn_white_eval = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0, 8: 5.0, 9: 5.0, 10: 5.0, 11: 5.0, 12: 5.0, 13: 5.0, 14: 5.0, 15: 5.0, 16: 1.0, 17: 1.0, 18: 2.0, 19: 3.0, 20: 3.0, 21: 2.0, 22: 1.0, 23: 1.0, 24: 0.5, 25: 0.5, 26: 1.0, 27: 2.5, 28: 2.5, 29: 1.0, 30: 0.5, 31: 0.5, 32: 0.0, 33: 0.0, 34: 0.0, 35: 2.0, 36: 2.0, 37: 0.0, 38: 0.0, 39: 0.0, 40: 0.5, 41: -0.5, 42: -1.0, 43: 0.0, 44: 0.0, 45: -1.0, 46: -0.5, 47: 0.5, 48: 0.5, 49: 1.0, 50: 1.0, 51: -2.0, 52: -2.0, 53: 1.0, 54: 1.0, 55: 0.5, 56: 0.0, 57: 0.0, 58: 0.0, 59: 0.0, 60: 0.0, 61: 0.0, 62: 0.0, 63: 0.0}
# pawn_black_eval = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0, 8: 0.5, 9: 1.0, 10: 1.0, 11: -2.0, 12: -2.0, 13: 1.0, 14: 1.0, 15: 0.5, 16: 0.5, 17: -0.5, 18: -1.0, 19: 0.0, 20: 0.0, 21: -1.0, 22: -0.5, 23: 0.5, 24: 0.0, 25: 0.0, 26: 0.0, 27: 2.0, 28: 2.0, 29: 0.0, 30: 0.0, 31: 0.0, 32: 0.5, 33: 0.5, 34: 1.0, 35: 2.5, 36: 2.5, 37: 1.0, 38: 0.5, 39: 0.5, 40: 1.0, 41: 1.0, 42: 2.0, 43: 3.0, 44: 3.0, 45: 2.0, 46: 1.0, 47: 1.0, 48: 5.0, 49: 5.0, 50: 5.0, 51: 5.0, 52: 5.0, 53: 5.0, 54: 5.0, 55: 5.0, 56: 0.0, 57: 0.0, 58: 0.0, 59: 0.0, 60: 0.0, 61: 0.0, 62: 0.0, 63: 0.0}


# kinight_white_eval = {0: -5.0, 1: -4.0, 2: -3.0, 3: -3.0, 4: -3.0, 5: -3.0, 6: -4.0, 7: -5.0, 8: -4.0, 9: -2.0, 10: 0.0, 11: 0.0, 12: 0.0, 13: 0.0, 14: -2.0, 15: -4.0, 16: -3.0, 17: 0.0, 18: 1.0, 19: 1.5, 20: 1.5, 21: 1.0, 22: 0.0, 23: -3.0, 24: -3.0, 25: 0.5, 26: 1.5, 27: 2.0, 28: 2.0, 29: 1.5, 30: 0.5, 31: -3.0, 32: -3.0, 33: 0.0, 34: 1.5, 35: 2.0, 36: 2.0, 37: 1.5, 38: 0.0, 39: -3.0, 40: -3.0, 41: 0.5, 42: 1.0, 43: 1.5, 44: 1.5, 45: 1.0, 46: 0.5, 47: -3.0, 48: -4.0, 49: -2.0, 50: 0.0, 51: 0.5, 52: 0.5, 53: 0.0, 54: -2.0, 55: -4.0, 56: -5.0, 57: -4.0, 58: -3.0, 59: -3.0, 60: -3.0, 61: -3.0, 62: -4.0, 63: -5.0}
# kight_black_eval = {0: -5.0, 1: -4.0, 2: -3.0, 3: -3.0, 4: -3.0, 5: -3.0, 6: -4.0, 7: -5.0, 8: -4.0, 9: -2.0, 10: 0.0, 11: 0.5, 12: 0.5, 13: 0.0, 14: -2.0, 15: -4.0, 16: -3.0, 17: 0.5, 18: 1.0, 19: 1.5, 20: 1.5, 21: 1.0, 22: 0.5, 23: -3.0, 24: -3.0, 25: 0.0, 26: 1.5, 27: 2.0, 28: 2.0, 29: 1.5, 30: 0.0, 31: -3.0, 32: -3.0, 33: 0.5, 34: 1.5, 35: 2.0, 36: 2.0, 37: 1.5, 38: 0.5, 39: -3.0, 40: -3.0, 41: 0.0, 42: 1.0, 43: 1.5, 44: 1.5, 45: 1.0, 46: 0.0, 47: -3.0, 48: -4.0, 49: -2.0, 50: 0.0, 51: 0.0, 52: 0.0, 53: 0.0, 54: -2.0, 55: -4.0, 56: -5.0, 57: -4.0, 58: -3.0, 59: -3.0, 60: -3.0, 61: -3.0, 62: -4.0, 63: -5.0}


# bishop_white_eval = {0: -2.0, 1: -1.0, 2: -1.0, 3: -1.0, 4: -1.0, 5: -1.0, 6: -1.0, 7: -2.0, 8: -1.0, 9: 0.0, 10: 0.0, 11: 0.0, 12: 0.0, 13: 0.0, 14: 0.0, 15: -1.0, 16: -1.0, 17: 0.0, 18: 0.5, 19: 1.0, 20: 1.0, 21: 0.5, 22: 0.0, 23: -1.0, 24: -1.0, 25: 0.5, 26: 0.5, 27: 1.0, 28: 1.0, 29: 0.5, 30: 0.5, 31: -1.0, 32: -1.0, 33: 0.0, 34: 1.0, 35: 1.0, 36: 1.0, 37: 1.0, 38: 0.0, 39: -1.0, 40: -1.0, 41: 1.0, 42: 1.0, 43: 1.0, 44: 1.0, 45: 1.0, 46: 1.0, 47: -1.0, 48: -1.0, 49: 0.5, 50: 0.0, 51: 0.0, 52: 0.0, 53: 0.0, 54: 0.5, 55: -1.0, 56: -2.0, 57: -1.0, 58: -1.0, 59: -1.0, 60: -1.0, 61: -1.0, 62: -1.0, 63: -2.0}
# bishop_black_eval = {0: -2.0, 1: -1.0, 2: -1.0, 3: -1.0, 4: -1.0, 5: -1.0, 6: -1.0, 7: -2.0, 8: -1.0, 9: 0.5, 10: 0.0, 11: 0.0, 12: 0.0, 13: 0.0, 14: 0.5, 15: -1.0, 16: -1.0, 17: 1.0, 18: 1.0, 19: 1.0, 20: 1.0, 21: 1.0, 22: 1.0, 23: -1.0, 24: -1.0, 25: 0.0, 26: 1.0, 27: 1.0, 28: 1.0, 29: 1.0, 30: 0.0, 31: -1.0, 32: -1.0, 33: 0.5, 34: 0.5, 35: 1.0, 36: 1.0, 37: 0.5, 38: 0.5, 39: -1.0, 40: -1.0, 41: 0.0, 42: 0.5, 43: 1.0, 44: 1.0, 45: 0.5, 46: 0.0, 47: -1.0, 48: -1.0, 49: 0.0, 50: 0.0, 51: 0.0, 52: 0.0, 53: 0.0, 54: 0.0, 55: -1.0, 56: -2.0, 57: -1.0, 58: -1.0, 59: -1.0, 60: -1.0, 61: -1.0, 62: -1.0, 63: -2.0}


# rook_white_eval = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0, 8: 0.5, 9: 1.0, 10: 1.0, 11: 1.0, 12: 1.0, 13: 1.0, 14: 1.0, 15: 0.5, 16: -0.5, 17: 0.0, 18: 0.0, 19: 0.0, 20: 0.0, 21: 0.0, 22: 0.0, 23: -0.5, 24: -0.5, 25: 0.0, 26: 0.0, 27: 0.0, 28: 0.0, 29: 0.0, 30: 0.0, 31: -0.5, 32: -0.5, 33: 0.0, 34: 0.0, 35: 0.0, 36: 0.0, 37: 0.0, 38: 0.0, 39: -0.5, 40: -0.5, 41: 0.0, 42: 0.0, 43: 0.0, 44: 0.0, 45: 0.0, 46: 0.0, 47: -0.5, 48: -0.5, 49: 0.0, 50: 0.0, 51: 0.0, 52: 0.0, 53: 0.0, 54: 0.0, 55: -0.5, 56: 0.0, 57: 0.0, 58: 0.0, 59: 0.5, 60: 0.5, 61: 0.0, 62: 0.0, 63: 0.0}
# rook_black_eval = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.5, 4: 0.5, 5: 0.0, 6: 0.0, 7: 0.0, 8: -0.5, 9: 0.0, 10: 0.0, 11: 0.0, 12: 0.0, 13: 0.0, 14: 0.0, 15: -0.5, 16: -0.5, 17: 0.0, 18: 0.0, 19: 0.0, 20: 0.0, 21: 0.0, 22: 0.0, 23: -0.5, 24: -0.5, 25: 0.0, 26: 0.0, 27: 0.0, 28: 0.0, 29: 0.0, 30: 0.0, 31: -0.5, 32: -0.5, 33: 0.0, 34: 0.0, 35: 0.0, 36: 0.0, 37: 0.0, 38: 0.0, 39: -0.5, 40: -0.5, 41: 0.0, 42: 0.0, 43: 0.0, 44: 0.0, 45: 0.0, 46: 0.0, 47: -0.5, 48: 0.5, 49: 1.0, 50: 1.0, 51: 1.0, 52: 1.0, 53: 1.0, 54: 1.0, 55: 0.5, 56: 0.0, 57: 0.0, 58: 0.0, 59: 0.0, 60: 0.0, 61: 0.0, 62: 0.0, 63: 0.0}


# queen_white_eval = {0: -2.0, 1: -1.0, 2: -1.0, 3: -0.5, 4: -0.5, 5: -1.0, 6: -1.0, 7: -2.0, 8: -1.0, 9: 0.0, 10: 0.0, 11: 0.0, 12: 0.0, 13: 0.0, 14: 0.0, 15: -1.0, 16: -1.0, 17: 0.0, 18: 0.5, 19: 0.5, 20: 0.5, 21: 0.5, 22: 0.0, 23: -1.0, 24: -0.5, 25: 0.0, 26: 0.5, 27: 0.5, 28: 0.5, 29: 0.5, 30: 0.0, 31: -0.5, 32: 0.0, 33: 0.0, 34: 0.5, 35: 0.5, 36: 0.5, 37: 0.5, 38: 0.0, 39: -0.5, 40: -1.0, 41: 0.5, 42: 0.5, 43: 0.5, 44: 0.5, 45: 0.5, 46: 0.0, 47: -1.0, 48: -1.0, 49: 0.0, 50: 0.5, 51: 0.0, 52: 0.0, 53: 0.0, 54: 0.0, 55: -1.0, 56: -2.0, 57: -1.0, 58: -1.0, 59: -0.5, 60: -0.5, 61: -1.0, 62: -1.0, 63: -2.0}
# queen_black_eval = {0: -2.0, 1: -1.0, 2: -1.0, 3: -0.5, 4: -0.5, 5: -1.0, 6: -1.0, 7: -2.0, 8: -1.0, 9: 0.0, 10: 0.0, 11: 0.0, 12: 0.0, 13: 0.5, 14: 0.0, 15: -1.0, 16: -1.0, 17: 0.0, 18: 0.5, 19: 0.5, 20: 0.5, 21: 0.5, 22: 0.5, 23: -1.0, 24: -0.5, 25: 0.0, 26: 0.5, 27: 0.5, 28: 0.5, 29: 0.5, 30: 0.0, 31: 0.0, 32: -0.5, 33: 0.0, 34: 0.5, 35: 0.5, 36: 0.5, 37: 0.5, 38: 0.0, 39: -0.5, 40: -1.0, 41: 0.0, 42: 0.5, 43: 0.5, 44: 0.5, 45: 0.5, 46: 0.0, 47: -1.0, 48: -1.0, 49: 0.0, 50: 0.0, 51: 0.0, 52: 0.0, 53: 0.0, 54: 0.0, 55: -1.0, 56: -2.0, 57: -1.0, 58: -1.0, 59: -0.5, 60: -0.5, 61: -1.0, 62: -1.0, 63: -2.0}


# king_white_eval = {0: -3.0, 1: -4.0, 2: -4.0, 3: -5.0, 4: -5.0, 5: -4.0, 6: -4.0, 7: -3.0, 8: -3.0, 9: -4.0, 10: -4.0, 11: -5.0, 12: -5.0, 13: -4.0, 14: -4.0, 15: -3.0, 16: -3.0, 17: -4.0, 18: -4.0, 19: -5.0, 20: -5.0, 21: -4.0, 22: -4.0, 23: -3.0, 24: -3.0, 25: -4.0, 26: -4.0, 27: -5.0, 28: -5.0, 29: -4.0, 30: -4.0, 31: -3.0, 32: -2.0, 33: -3.0, 34: -3.0, 35: -4.0, 36: -4.0, 37: -3.0, 38: -3.0, 39: -2.0, 40: -1.0, 41: -2.0, 42: -2.0, 43: -2.0, 44: -2.0, 45: -2.0, 46: -2.0, 47: -1.0, 48: 2.0, 49: 2.0, 50: 0.0, 51: 0.0, 52: 0.0, 53: 0.0, 54: 2.0, 55: 2.0, 56: 2.0, 57: 3.0, 58: 1.0, 59: 0.0, 60: 0.0, 61: 1.0, 62: 3.0, 63: 2.0}
# king_black_eval = {0: 2.0, 1: 3.0, 2: 1.0, 3: 0.0, 4: 0.0, 5: 1.0, 6: 3.0, 7: 2.0, 8: 2.0, 9: 2.0, 10: 0.0, 11: 0.0, 12: 0.0, 13: 0.0, 14: 2.0, 15: 2.0, 16: -1.0, 17: -2.0, 18: -2.0, 19: -2.0, 20: -2.0, 21: -2.0, 22: -2.0, 23: -1.0, 24: -2.0, 25: -3.0, 26: -3.0, 27: -4.0, 28: -4.0, 29: -3.0, 30: -3.0, 31: -2.0, 32: -3.0, 33: -4.0, 34: -4.0, 35: -5.0, 36: -5.0, 37: -4.0, 38: -4.0, 39: -3.0, 40: -3.0, 41: -4.0, 42: -4.0, 43: -5.0, 44: -5.0, 45: -4.0, 46: -4.0, 47: -3.0, 48: -3.0, 49: -4.0, 50: -4.0, 51: -5.0, 52: -5.0, 53: -4.0, 54: -4.0, 55: -3.0, 56: -3.0, 57: -4.0, 58: -4.0, 59: -5.0, 60: -5.0, 61: -4.0, 62: -4.0, 63: -3.0}
