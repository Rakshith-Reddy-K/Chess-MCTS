import chess
import chess.pgn
import chess.engine
from game import Game
from view import View
import mcts as MCTS
from eval import evaluate,evaluateAB,evaluateMove
import copy
from evaluation import getScore
import time

engine = chess.engine.SimpleEngine.popen_uci(r'/Users/rakshithreddy/Desktop/chess_mcts/stockfish 2/stockfish-macos-m1-apple-silicon')

def main():
    board = chess.Board()
    pgn = []
    game = Game()
    view = View(game.getBoard())
    # move = chess.Move.from_uci("h2h3")
    # info = engine.analyse(board, chess.engine.Limit(time=0.0001))
    # score = str(info['score'].white())
    # print(evaluateMove(move,board),score)
    # board.push_san("h2h3")
    # # print("Evaluate AB ->>>>>",evaluateAB(board))
    # # print("Evaluate ->>>>>",evaluate(board))
    # move = chess.Move.from_uci("e7e5")
    # info = engine.analyse(board, chess.engine.Limit(time=0.0001))
    # score = str(info['score'].white())
    # print(evaluateMove(move,board),score)
    # board.push_san("e7e5")
    # # print("Evaluate AB ->>>>>",evaluateAB(board))
    # # print("Evaluate ->>>>>",evaluate(board))
    # move = chess.Move.from_uci("d2d3")
    # info = engine.analyse(board, chess.engine.Limit(time=0.0001))
    # score = str(info['score'].white())
    # print(evaluateMove(move,board),score)
    # board.push_san("d2d3")
    # # print("Evaluate AB ->>>>>",evaluateAB(board))
    # # print("Evaluate ->>>>>",evaluate(board))
    # move = chess.Move.from_uci("d7d6")
    # info = engine.analyse(board, chess.engine.Limit(time=0.0001))
    # score = str(info['score'].white())
    # print(evaluateMove(move,board),score)
    # board.push_san("d7d6")
    # # print("Evaluate AB ->>>>>",evaluateAB(board))
    # # print("Evaluate ->>>>>",evaluate(board))
    # move = chess.Move.from_uci("c1f4")
    # info = engine.analyse(board, chess.engine.Limit(time=0.0001))
    # score = str(info['score'].white())
    # print(evaluateMove(move,board),score)
    # board.push_san("c1f4")
    # move = chess.Move.from_uci("d8g5")
    # info = engine.analyse(board, chess.engine.Limit(time=0.0001))
    # score = str(info['score'].white())
    # print(evaluateMove(move,board),score)
    # board.push_san("d8g5")
    # info = engine.analyse(board, chess.engine.Limit(time=0.0001))
    # score = str(info['score'].white())
    # print(score,evaluateAB(board))
    # print("Evaluate AB ->>>>>",evaluateAB(board))
    # print("Evaluate ->>>>>",evaluate(board))
    # board.push_san("e2e4")
    # board.push_san("g8h6")
    # s=0
    # for move in board.legal_moves:
    #     curr_board = copy.deepcopy(board)
    #     move_str = curr_board.san(move)
    #     curr_board.push_san(move_str)
    #     s=s+getScore(curr_board,chess.WHITE)
    #     print(move ," -----> ", getScore(curr_board,chess.WHITE))
    # print("S",s)
    while((not board.is_game_over()) and (not board.is_fivefold_repetition()) and (len(pgn) < 160)):
        start_time = time.time()
        nextMove = MCTS.predictNextMove(board,1000)
        move_str = board.san(nextMove)
        board.push_san(move_str)
        pgn.append(move_str)
        game.playMove(move_str)
        view.update()
        print(f"move - {nextMove.uci()}, eval - {eval}, Time taken to run: {time.time() - start_time:.6f} seconds")
    print("game over!")
    print(game.outcome())
    print(' '.join(pgn))
    return
if __name__ == '__main__':
    main()
    exit()