import numpy as np
from chess import Board
import math
exploration_factor = 1.4
class Node:
    def __init__(self,board:Board,move,parent = None):
        self.board = board
        self.legal_moves = list(board.legal_moves) if board.legal_moves is not None else []
        self.parent = parent
        self.move = move
        self.children = {}
        self.expanded = False
        self.children_values = np.zeros([len(self.legal_moves)], dtype=np.float32)
        self.children_number_visits = np.zeros([len(self.legal_moves)], dtype=np.float32)
    
    @property
    def number_visits(self):
        return self.parent.children_number_visits[self.move]

    @number_visits.setter
    def number_visits(self, value):
        self.parent.children_number_visits[self.move] = value

    @property
    def total_value(self):
        return self.parent.children_values[self.move]

    @total_value.setter
    def total_value(self, value):
        self.parent.children_values[self.move] = value

    def children_avg_rewards(self):  
        return self.children_values / (1 + self.children_number_visits)

    def children_expl_values(self):
        if self.parent is None:
            total_visits = np.sum(self.children_number_visits)
            return exploration_factor * np.sqrt(total_visits / (1.0 + self.children_number_visits))
        return  exploration_factor * np.sqrt(math.log(self.number_visits) / (1.0 + self.children_number_visits))

    def best_child(self):
        return np.argmax(self.children_avg_rewards() + self.children_expl_values())

    def isRoot(self):
        return self.parent is None