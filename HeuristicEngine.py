import random
import math
from Piece import Piece

class LaneEvaluation:
    def __init__(self, lane):
        self.num_player_matching = 0
        self.num_opponent_matching = 0 
        self.lane_values = [board.board[cell[0]][cell[1]] for cell in lane]
        self.num_blanks = lane_values.count(" ")

        danger_ratings = [0] * len(self.opponent.pieces)

        if num_blanks == 4:
            return

        common_positive_bitmask = 15
        common_negative_bitmask = 15

        for cell in lane_values:
            if cell != " ":
                common_positive_bitmask &= cell.type_bitmask
                common_negative_bitmask &= ~cell.type_bitmask

        # if there is no common type bitmask, then at least
        # one piece is disjoint, and it is impossible to win
        # in this lane
        if common_positive_bitmask == 0 and common_negative_bitmask == 0:
            return
class HeuristicEngine:
    def __init__(self, player, opponent):
        self.opponent = opponent
        self.player = player
        self.opponent_piece_dangers = [0] * len(self.opponent.pieces)
