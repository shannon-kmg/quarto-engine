import random
import math
from Piece import Piece
from HeuristicEngine import HeuristicEngine

class Node:
    def __init__(self, board, piece, cell):
        self.board = board
        self.piece = piece
        self.cell = cell

class PlayerMiniMax:
    def __init__(self, q, opponent):
        self.q = q
        self.player_name = "Q" if q else "G"
        self.pieces = []
        self.opponent = opponent
        self.opponent_piece_ratings = [0] * len(self.opponent.pieces)
        for i in range(0, 8) if not q else range(8, 16):
            b_string = format(i, "04b")
            arg_list = [not not int(c) for c in b_string]
            self.pieces.append(Piece(*arg_list))
        # Heuristic engine set to always maximize q's score
        self.he = HeuristicEngine(self, self.opponent) if self.q else HeuristicEngine(self.opponent, self)

    def remove_piece(self, index):
        p = self.pieces[index]
        del self.pieces[index]
        return p

    def select_opponent_piece(self, _):
        return self.he.pop_danger(self.he.get_least_dangerous())

    def draw_pieces(self):
        print([p.draw() for p in self.pieces])

    def move(self, board, piece):
        best_cell = self.minimax(Node(board, piece), 2, self.q)
        board.place(piece, best_cell[0], best_cell[1])

    def minimax(self, node, depth, q):
        if depth == 0 or node.board.check_win() or node.board.check_draw():
            return (self.he.calc_board_score(node.board, node.piece), node)
        valid_cells = node.board.valid_cells()
        if q:
            value = (-math.inf, None)
            for piece in self.pieces:
                for cell in valid_cells:
                    board.place(piece, cell[0], cell[1])
                    for o_piece in self.opponent.pieces:
                        value = max(value, minimax(Node(board, o_piece, cell), depth - 1, False))
                    board.unplace(cell[0], cell[1])
            return value
        else:
            value = (math.inf, None)
            for piece in self.pieces:
                for cell in valid_cells:
                    board.place(piece, cell[0], cell[1])
                    for o_piece in self.opponent.pieces:
                        value = min(value, minimax(Node(board, o_piece, cell), depth - 1, True))
                    board.unplace(cell[0], cell[1])
            return value
