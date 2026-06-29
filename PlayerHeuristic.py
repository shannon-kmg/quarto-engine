import random
import math
from Piece import Piece
class PlayerHeuristic:
    def __init__(self, q, opponent):
        self.player_name = "Q" if q else "G"
        self.pieces = []
        self.opponent = opponent
        self.opponent_piece_ratings = {}
        for i in range(0, 8) if not q else range(8, 16):
            b_string = format(i, "04b")
            arg_list = [not not int(c) for c in b_string]
            self.pieces.append(Piece(*arg_list))

    def remove_piece(self, index):
        p = self.pieces[index]
        del self.pieces[index]
        return p

    def select_opponent_piece(self, _):
        print(self.opponent_piece_ratings)
        min_danger = math.inf
        best_piece_index = 0
        for index, rating in self.opponent_piece_ratings.items():
            if rating < min_danger:
                min_danger = rating
                best_piece_index = index

        return self.opponent.remove_piece(best_piece_index)

    def draw_pieces(self):
        print([p.draw() for p in self.pieces])

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
        if common_positive_bitmask == 0 or common_negative_bitmask == 0:
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

        for piece_index, piece in enumerate(self.opponent.pieces):
            if piece.type_bitmask & common_positive_bitmask != 0 or ~piece.type_bitmask & common_negative_bitmask != 0:
                if num_blanks == 3:
                    if num_opponent_matching >= 3:
                        self.opponent_piece_ratings[piece_index] += 10
                if num_blanks == 2:
                    if num_self_matching >= 3:
                        self.opponent_piece_ratings[piece_index] += 1
                    else:
                        self.opponent_piece_ratings[piece_index] += 1
                if num_blanks == 1:
                    self.opponent_piece_ratings[piece_index] += math.inf

        if num_blanks == 3:
            if num_opponent_matching >= 3:
                score -= 2
            elif num_opponent_matching >= 2:
                score -= 1
            # this is 3 instead of 2 because the peice we
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

    def move(self, board, piece):
        valid_cells = board.valid_cells()
        best_cell = random.choice(valid_cells)
        best_score = -math.inf

        lanes = board.get_lanes()

        for piece_index, _ in enumerate(self.opponent.pieces):
            self.opponent_piece_ratings[piece_index] = 0

        for cell in valid_cells:
            score = 0
            board.place(piece, cell[0], cell[1])
            for lane in board.get_coord_lanes():
                if cell in lane:
                    score += self.evaluate_lane(lane, board)
            board.unplace(cell[0], cell[1])
            if score > best_score:
                best_score = score
                best_cell = cell

        board.place(piece, best_cell[0], best_cell[1])
