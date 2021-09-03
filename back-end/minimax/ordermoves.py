import chess

def order_moves(board):

    move_scores = []
    
    moves = list(board.legal_moves)

    for move in moves:
        move_score_guess = 0
        move_piece_type = str(board.piece_at(
            eval('chess.' + str(move)[:2].upper())))
        capture_piece_type = str(board.piece_at(
            eval('chess.' + str(move)[2:].upper())))

        if capture_piece_type != 'None':
            move_score_guess = 10 * \
                get_piece_value(capture_piece_type) - \
                get_piece_value(move_piece_type)

        move_scores.append([move, move_score_guess])
    
    move_scores = sorted(move_scores, key=lambda k: k[1], reverse = True)
    
    return [move[0] for move in move_scores]
    
def get_piece_value(piece):
    if(piece == 'None'):
        return 0
    elif(piece.upper() == 'P'):
        return 10
    elif(piece.upper() == 'N'):
        return 30
    elif(piece.upper() == 'B'):
        return 30
    elif(piece.upper() == 'R'):
        return 50
    elif(piece.upper() == 'Q'):
        return 90
    elif(piece.upper() == 'K'):
        return 900
