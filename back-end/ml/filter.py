import numpy as np
import chess

def filter_good_moves(board, classifier, first_print):
    moves = []
    good_moves = []
    for move in list(board.legal_moves):
        board_features = get_board_features(board)
        from_square, to_square = get_move_features(move)
        line = np.concatenate((board_features, from_square, to_square))

        move_translated = np.array(["%.1f" % number for number in line])
        good_move_prob = classifier.predict_proba(move_translated.astype(np.float64).reshape(1, -1))[0][1]
        if good_move_prob > 0.35:
            good_moves.append([move, good_move_prob])
        moves.append([move, good_move_prob])
        #print(move, self.classifier.predict(move_translated.reshape(1, -1)), self.classifier.predict_proba(move_translated.reshape(1, -1)))
    moves = sorted(moves, key=lambda k: k[1], reverse = True) 
    if first_print:
        print("Ordered moves")
        for move in moves:
            print(f'{move[0]}: {move[1]}')

        print("Good Moves:")
        for move in good_moves:
            print(f'{move[0]}: {move[1]}')

    if len(good_moves) == 0:
        moves = [move[0] for move in moves]
        return moves if int(len(moves)) <= 5 else moves[:5]

    good_moves = [move[0] for move in good_moves]
    return good_moves if int(len(good_moves) * 0.25) <= 5 else good_moves[:int(len(good_moves) * 0.25)]

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