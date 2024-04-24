import chess
import torch
import numpy as np
import consts

endGame = False
model = torch.jit.load('scripted.pt')
model.eval()

def getPositionalValue(sq: chess.Square, pc: chess.Piece, endGame: bool) -> float:
    if pc.color == chess.BLACK:
        sq ^= 56
    if pc.piece_type == chess.KING:
        if endGame:
            return consts.king_end_game_table[sq]
        else:
            return consts.king_middle_game_table[sq]
    return consts.piecePositionalScore[pc.piece_type][sq]

def get_game_phase(pieceMap):
    minor_pieces = 0
    queens = 0
    for _, piece in pieceMap:
        if piece.piece_type == chess.BISHOP or piece.piece_type == chess.BISHOP:
            minor_pieces += 1
        elif piece.piece_type == chess.QUEEN:
            queens += 1
    return minor_pieces < 2 or queens == 0

def evaluateMove(mv: chess.Move, board: chess.Board):
    white = 1
    if board.turn == chess.BLACK:
        white = -1
    matDiff = 0
    if mv.promotion:
        return float('inf') * white
    pc = board.piece_at(mv.from_square)
    posChange = getPositionalValue(mv.to_square, pc, endGame) - getPositionalValue(mv.from_square, pc, endGame)
    if board.is_capture(mv):
        matDiff = evalCapture(mv, board)
    val = posChange + matDiff
    return val * white
 
def evalCapture(mv: chess.Move, board: chess.Board):
    if board.is_en_passant(mv):
        return consts.pieceValue[chess.PAWN]
    return consts.pieceValue[board.piece_at(mv.to_square).piece_type] - consts.pieceValue[board.piece_at(mv.from_square).piece_type]

def evalPiece(sq: chess.Square, pc: chess.Piece, endGame: bool) -> float:
    return getPositionalValue(sq, pc, endGame) + consts.pieceValue[pc.piece_type]

def evaluateAB(board: chess.Board) -> float:
    pieceMap = board.piece_map().items()
    global endGame
    if endGame == False:
        endGame = get_game_phase(pieceMap)
    white = 1
    score = 0
    if board.turn == chess.BLACK:
        white = -1
    
    for sq, pc in pieceMap:
        eval = evalPiece(sq, pc, endGame)
        if pc.color == chess.WHITE:
            score += eval
        else:
            score -= eval
    return score * white

def evaluate(board: chess.Board):
    x = torch.tensor(fen_to_features(board.fen()))
    with torch.no_grad():
        y_hat_eval = model(x).squeeze()
    if board.turn == chess.BLACK:
        y_hat_eval = -y_hat_eval
    return y_hat_eval

def fen_to_features(fen):
    piece_to_index = {'r': 0, 'n': 1, 'b': 2, 'q': 3, 'k': 4, 'p': 5,
                      'P': 6, 'K': 7, 'Q': 8, 'B': 9, 'N': 10, 'R': 11}

    one_hot_board = np.zeros((8, 8, 13), dtype=np.float32)
    additional_features = np.zeros(13, dtype=np.float32)
    # additional_features = np.zeros(1, dtype=np.float32)

    fen_rows = fen.split()[0].split('/')
    for row_idx, row in enumerate(fen_rows):
        col_idx = 0
        for char in row:
            if char.isdigit():
                col_idx += int(char)
            elif char in piece_to_index:
                piece_idx = piece_to_index[char]
                one_hot_board[row_idx, col_idx, piece_idx] = -1
                if piece_to_index[char] > 5:
                  one_hot_board[row_idx, col_idx, piece_idx] = 1
                col_idx += 1
    turn_index = 12
    one_hot_board[:, :, turn_index].fill(1)
    if fen.split()[1] == 'b':
#         print(f'Reached 1 {fen}')
        one_hot_board[:, :, turn_index].fill(-1)
#         one_hot_board = np.rot90(one_hot_board, k = 2)
#     additional_features[0] = 1 if fen[1] == 'w' else 0
    additional_features[0:4] = [int(right in fen.split()[2]) for right in ['K', 'Q', 'k', 'q']]
    if fen.split()[3] != '-':
        en_passant_row = ord(fen.split()[3][0]) - ord('a')
        additional_features[5 + en_passant_row] = 1
    return np.concatenate([one_hot_board.flatten(), additional_features])
