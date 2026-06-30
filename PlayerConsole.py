from Piece import Piece


class PlayerConsole:
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
        print("{}, select a piece for your opponent:".format(self.player_name))
        opponent.draw_pieces()
        index = int(input(""))
        return opponent.remove_piece(index)

    def draw_pieces(self):
        print([p.draw() for p in self.pieces])

    def move(self, board, piece):
        print(
            "{}, its your turn to move. You are placing: {}".format(
                self.player_name, piece.draw()
            )
        )
        row = int(input("Enter row: ".format(self.player_name)))
        col = int(input("Enter col: ".format(self.player_name)))
        while not board.place(piece, row, col):
            print("Invalid move, try again")
            self.move(board, piece)
