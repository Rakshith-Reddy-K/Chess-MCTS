import chess
import chess.pgn
import chess.engine
from eval import evaluate,evaluateAB
chess.engine.Score
engine = chess.engine.SimpleEngine.popen_uci(r'/Users/rakshithreddy/Desktop/chess_mcts/stockfish 2/stockfish-macos-m1-apple-silicon')
def convert_mate_to_score(mateScore):
    score = int(mateScore[1:])
    sign = -1 if score < 0 else 1 if score > 0 else 0
    if score == 0:
        score = 1000
    else:
        score = (1000 - (abs(score) * 0.5)) * sign
    return score

def getScore(board: chess.Board,turn):
    # pov = -1 if turn is chess.BLACK else 1
    # 1 Stockfish evaluation
    parentTurn = chess.BLACK if board.turn == chess.WHITE else chess.WHITE
    info = engine.analyse(board, chess.engine.Limit(depth=6))
    score = None
    if turn == chess.BLACK:
        score = str(info['score'].black())
    else:
        score = str(info['score'].white())
    if info['score'].is_mate() :
        score = convert_mate_to_score(score)
    else :
        score = int(score)
    score = score/100
    if score >= 10:
        score = 5
    elif score >= 7.5:
        score = 4
    elif score >= 5:
        score = 3
    elif score >=3.5:
        score = 2
    elif score >= 2:
        score = 1
    elif score <= -10:
        score = -5
    elif score <= -7.5:
        score = -4
    elif score <= -5:
        score = -3
    elif score <= -3.5:
        score= -2
    elif score <= -2:
        score = -1
    else:
        score = score/5
    # print("Mate ",str(info['score'].white()),info['score'].is_mate(), pov * score)
    if turn != parentTurn:
        score *= -1
    return score * 3
    if "#" in score :
        score = score[1:]
        score = int(score) * 100
    else :
        score = int(score)
    score = score/20
    return pov * score
    #  2 DNN
    return pov * evaluate(board)
    # 3 Alpha-beta evaluation function
    # score =  evaluateAB(board)
    # return score

