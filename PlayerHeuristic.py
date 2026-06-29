import random
import math
from Piece import Piece
from HeuristicEngine import HeuristicEngine
class PlayerHeuristic:
    def __init__(self, q, opponent):
        self.player_name = "Q" if q else "G"
        self.pieces = []
        self.opponent = opponent
        self.opponent_piece_ratings = [0] * len(self.opponent.pieces)
        for i in range(0, 8) if not q else range(8, 16):
            b_string = format(i, "04b")
            arg_list = [not not int(c) for c in b_string]
            self.pieces.append(Piece(*arg_list))
        self.he = HeuristicEngine(self, self.opponent)

    def remove_piece(self, index):
        p = self.pieces[index]
        del self.pieces[index]
        return p

    def select_opponent_piece(self, _):
        return self.he.pop_danger(self.he.get_least_dangerous())

    def draw_pieces(self):
        print([p.draw() for p in self.pieces])

    def move(self, board, piece):
        best_cell = self.he.get_best_move(board, piece)
        board.place(piece, best_cell[0], best_cell[1])
