import random
import math
from Piece import Piece
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

    def remove_piece(self, index):
        p = self.pieces[index]
        del self.pieces[index]
        return p

    def select_opponent_piece(self, _):
        print(self.opponent.pieces)
        print(self.opponent_piece_ratings)
        min_danger = math.inf
        best_piece_index = 0
        for index, rating in enumerate(self.opponent_piece_ratings):
            if rating < min_danger:
                min_danger = rating
                best_piece_index = index

        del self.opponent_piece_ratings[best_piece_index]
        return self.opponent.remove_piece(best_piece_index)

    def draw_pieces(self):
        print([p.draw() for p in self.pieces])

    def calculate_opponent_danger(self, lane, board):
        lane_values = [board.board[cell[0]][cell[1]] for cell in lane]
        num_blanks = lane_values.count(" ")

        if len(self.opponent.pieces) == 0:
            return [0]
        
        danger_ratings = [0] * len(self.opponent.pieces)

        if num_blanks == 4:
            return danger_ratings
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
            return danger_ratings

        num_opponent_matching = 0
        num_self_matching = 0
        for piece in self.opponent.pieces:
            if piece.type_bitmask & common_positive_bitmask != 0:
                num_opponent_matching += 1

            if ~piece.type_bitmask & common_negative_bitmask != 0:
                num_opponent_matching += 1

        for piece in self.pieces:
            if piece.type_bitmask & common_positive_bitmask != 0:
                num_self_matching += 1

            if ~piece.type_bitmask & common_negative_bitmask != 0:
                num_self_matching += 1

        for piece_index, piece in enumerate(self.opponent.pieces):
            if piece.type_bitmask & common_positive_bitmask != 0 or ~piece.type_bitmask & common_negative_bitmask != 0:
                if num_blanks == 3:
                    if num_opponent_matching >= 3:
                        danger_ratings[piece_index] += 10
                if num_blanks == 2:
                    if num_self_matching >= 2:
                        danger_ratings[piece_index] -= 1
                    else:
                        danger_ratings[piece_index] += 1
                if num_blanks == 1:
                    danger_ratings[piece_index] += math.inf
        return danger_ratings

    def evaluate_lane(self, lane, board):
        score = 0
        # assming we have just played in this lane
        lane_values = [board.board[cell[0]][cell[1]] for cell in lane]
        num_blanks = lane_values.count(" ")

        # this calculation only works if we always assume
        # there is a piece in this lane
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
#            print("DISJOINT", lane_values, common_positive_bitmask, common_negative_bitmask)
            return 0

        num_opponent_matching = 0
        num_self_matching = 0
        for piece in self.opponent.pieces:
            if piece.type_bitmask & common_positive_bitmask != 0:
                num_opponent_matching += 1

            if ~piece.type_bitmask & common_negative_bitmask != 0:
                num_opponent_matching += 1

        for piece in self.pieces:
            if piece.type_bitmask & common_positive_bitmask != 0:
                num_self_matching += 1

            if ~piece.type_bitmask & common_negative_bitmask != 0:
                num_self_matching += 1

        if num_blanks == 3:
            if num_opponent_matching >= 3:
                score -= 2
            elif num_opponent_matching >= 2:
                score -= 1
            # this is 3 instead of 2 because the piece we
            # are considering placing has not been removed
            # from our rack yet.
            elif num_self_matching >= 3: 
                score += 1
        if num_blanks == 2:
            if num_self_matching >= 2:
                score += 10
            elif num_opponent_matching >= 2:
                score -= 10
        if num_blanks == 1:
            if num_opponent_matching >= 1:
                score -= 100
            elif num_self_matching >= 1:
                score += 100

        return score

    def update_piece_ratings(self, dangers):
        if len(self.opponent_piece_ratings) == 0:
            return
        for i, d in enumerate(dangers):
            self.opponent_piece_ratings[i] += d

    def move(self, board, piece):
        valid_cells = board.valid_cells()
        best_cell = random.choice(valid_cells)
        best_score = -math.inf

        self.opponent_piece_ratings = [0] * len(self.opponent.pieces)

        for cell in valid_cells:
            score = 0
            for lane in board.get_coord_lanes():
                if cell in lane:
                    cur_dangers = self.calculate_opponent_danger(lane, board)
                    self.update_piece_ratings(cur_dangers)
                    board.place(piece, cell[0], cell[1])
                    score += self.evaluate_lane(lane, board)
                    est_dangers = self.calculate_opponent_danger(lane, board)
                    board.unplace(cell[0], cell[1])
                    score += (min(cur_dangers) - min(est_dangers))
            if score > best_score:
                best_score = score
                best_cell = cell

        board.place(piece, best_cell[0], best_cell[1])
