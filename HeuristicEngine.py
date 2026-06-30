import random
import math
from Piece import Piece

class LaneEvaluation:
    def __init__(self, lane, player, opponent, board):
        self.player = player
        self.opponent = opponent
        self.num_player_matching = 0
        self.num_opponent_matching = 0 
        self.lane_values = [board.board[cell[0]][cell[1]] for cell in lane]
        self.num_blanks = self.lane_values.count(" ")

        danger_ratings = [0] * len(self.opponent.pieces)

        self.common_positive_bitmask = 15
        self.common_negative_bitmask = 15

        for cell in self.lane_values:
            if cell != " ":
                self.common_positive_bitmask &= cell.type_bitmask
                self.common_negative_bitmask &= ~cell.type_bitmask

        # if there is no self.common type bitmask, then at least
        # one piece is disjoint, and it is impossible to win
        # in this lane
        if self.common_positive_bitmask == 0 and self.common_negative_bitmask == 0:
            return

        for piece in self.opponent.pieces:
            if piece.type_bitmask & self.common_positive_bitmask != 0:
                self.num_opponent_matching += 1

            if ~piece.type_bitmask & self.common_negative_bitmask != 0:
                self.num_opponent_matching += 1

        for piece in self.player.pieces:
            if piece.type_bitmask & self.common_positive_bitmask != 0:
                self.num_player_matching += 1

            if ~piece.type_bitmask & self.common_negative_bitmask != 0:
                self.num_player_matching += 1

class HeuristicEngine:
    def __init__(self, player, opponent):
        self.opponent = opponent
        self.player = player
        self.opponent_piece_dangers = [0] * len(self.opponent.pieces)

    def get_least_dangerous(self):
        min_danger = math.inf
        best_piece_index = 0
        print(self.opponent.pieces)
        print(self.opponent_piece_dangers)
        for index, rating in enumerate(self.opponent_piece_dangers):
            if rating < min_danger:
                min_danger = rating
                best_piece_index = index

        return best_piece_index

    def pop_danger(self, index):
        del self.opponent_piece_dangers[index]
        return self.opponent.remove_piece(index)
    
    def score_lane(self, lane, board):
        score = 0
        le = LaneEvaluation(lane, self.player, self.opponent, board)

        if le.num_blanks == 0:
            return math.inf

        if le.num_blanks == 3:
            if le.num_opponent_matching >= 3:
                score -= 2
            elif le.num_opponent_matching >= 2:
                score -= 1
            # this is 3 instead of 2 because the piece we
            # are considering placing has not been removed
            # from our rack yet.
            elif le.num_player_matching >= 3: 
                score += 1
        if le.num_blanks == 2:
            if le.num_player_matching >= 2:
                score += 10
            elif le.num_opponent_matching >= 2:
                score -= 10
        if le.num_blanks == 1:
            if le.num_opponent_matching >= 1:
                score -= 100
            elif le.num_player_matching >= 1:
                score += 100

        return score

    def calculate_opponent_danger(self, lane, board):
        le = LaneEvaluation(lane, self.player, self.opponent, board)
        if len(self.opponent.pieces) == 0:
            return [0]

        danger_ratings = [0] * len(self.opponent.pieces)


        if le.num_blanks == 4:
            return danger_ratings

        for piece_index, piece in enumerate(self.opponent.pieces):
            if piece.type_bitmask & le.common_positive_bitmask != 0 or ~piece.type_bitmask & le.common_negative_bitmask != 0:
                if le.num_blanks == 3:
                    if le.num_opponent_matching >= 3:
                        danger_ratings[piece_index] += 10
                if le.num_blanks == 2:
                    if le.num_player_matching >= 2:
                        danger_ratings[piece_index] -= 1
                    elif le.num_opponent_matching >= 2:
                        danger_ratings[piece_index] += 1
                if le.num_blanks == 1:
                    danger_ratings[piece_index] += math.inf
        return danger_ratings

    def update_piece_dangers(self, dangers):
        if len(self.opponent_piece_dangers) == 0:
            return
        for i, d in enumerate(dangers):
            self.opponent_piece_dangers[i] += d

    def get_best_move(self, board, piece):
        valid_cells = board.valid_cells()
        best_cell = random.choice(valid_cells)
        best_score = -math.inf

        self.opponent_piece_dangers = [0] * len(self.opponent.pieces)

        for cell in valid_cells:
            score = 0
            for lane in board.get_coord_lanes():
                if cell in lane:
                    cur_dangers = self.calculate_opponent_danger(lane, board)
                    self.update_piece_dangers(cur_dangers)
                    board.place(piece, cell[0], cell[1])
                    score += self.score_lane(lane, board)
                    est_dangers = self.calculate_opponent_danger(lane, board)
                    board.unplace(cell[0], cell[1])
                    score += (min(cur_dangers) - min(est_dangers))
            if score > best_score:
                best_score = score
                best_cell = cell

        return best_cell
