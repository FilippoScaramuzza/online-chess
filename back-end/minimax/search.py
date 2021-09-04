from . import evaluate
from . import ordermoves
import sys

sys.path.append('..')
from ml.filter import filter_good_moves

def search(depth, alpha, beta, board, is_ai_white, with_ml, classifier):
    if depth == 0:
        return quiescence(alpha, beta, board, with_ml, classifier)
        #return quiescence(alpha, beta, board, is_ai_white, with_ml, classifier)

    #moves = ordermoves.order_moves(board)
    if with_ml:
        moves = filter_good_moves(board=board, classifier=classifier, first_print=False)
    else:
        moves = list(board.legal_moves)

    if len(list(moves)) == 0:
        if board.is_checkmate():
            return 9999

        return 0

    for move in moves:
        board.push(move)
        evaluation = -search(depth - 1, -beta, -alpha, board, is_ai_white, with_ml, classifier)
        board.pop()

        if evaluation >= beta:
            return beta

        alpha = max(alpha, evaluation)

    return alpha

    
def quiescence(alpha, beta, board, with_ml, classifier):
    stand_pat = evaluate.evaluate(board)
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat

    if not with_ml:
        moves = filter_good_moves(board=board, classifier=classifier, first_print=False)
    else:
        moves = list(board.legal_moves)

    for move in moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiescence(-beta, -alpha, board, with_ml, classifier)
            board.pop()

            if (score >= beta):
                return beta
            if (score > alpha):
                alpha = score
    return alpha
# def search(depth, alpha, beta, board, is_ai_white, is_maximizing_player):
#     '''
#         Get the evaluation for a specific move. This is recursive.
#     '''
#     if(depth == 0):
#         # When minimax reaches depth 0, it returns the evaluation of the move.
#         return - evaluate.evaluate(board, is_ai_white)
    
#     legal_moves = board.legal_moves

#     if(is_maximizing_player):
#         best_move = -9999
#         for move in legal_moves:
#             board.push(move)
#             best_move = max(best_move, search(depth=depth-1,
#                                                     alpha=alpha,
#                                                     beta=beta,
#                                                     board=board,
#                                                     is_ai_white=is_ai_white,
#                                                     is_maximizing_player=not is_maximizing_player))
#             board.pop()
#             alpha = max(alpha, best_move)
#             if(beta <= alpha):
#                 return best_move
#         return best_move
#     else:
#         best_move = 9999
#         for move in legal_moves:
#             board.push(move)
#             best_move = min(best_move, search(depth=depth-1,
#                                                     alpha=alpha,
#                                                     beta=beta,
#                                                     board=board,
#                                                     is_ai_white=is_ai_white,
#                                                     is_maximizing_player=not is_maximizing_player))
#             board.pop()
#             beta = min(beta, best_move)
#             if(beta <= alpha):
#                 return best_move
#         return best_move
