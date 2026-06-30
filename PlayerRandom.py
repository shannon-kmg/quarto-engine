import random
from Piece import Piece


class PlayerRandom:
    def __init__(self, q):
        self.player_name = "Q" if q else "G"
        self.pieces = []
        for i in range(0, 8) if not q else range(8, 16):
            b_string = format(i, "04b")
            arg_list = [not not int(c) for c in b_string]
            self.pieces.append(Piece(*arg_list))

    def remove_piece(self, index):
        p = self.pieces[index]
        del self.pieces[index]
        return p

    def select_opponent_piece(self, opponent):
        index = random.randint(0, len(opponent.pieces) - 1)
        return opponent.remove_piece(index)

    def draw_pieces(self):
        print([p.draw() for p in self.pieces])

    def move(self, board, piece):
        pos = random.choice(board.valid_cells())
        board.place(piece, pos[0], pos[1])
