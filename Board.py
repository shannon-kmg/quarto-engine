class Board:
    def __init__(self):
        self.board = [[" " for x in range(4)] for x in range(4)]

    def valid_cells(self):
        cells = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == " ":
                    cells.append((i, j))
        return cells

    def draw(self):
        for i in range(len(self.board)):
            print("|", end="")
            for j in range(len(self.board[0])):
                if self.board[i][j] != " ":
                    print(self.board[i][j].draw() + "|", end="")
                else:
                    print(" |", end="")
            print("")

    def place(self, piece, row, col):
        if row > 3 or col > 3 or self.board[row][col] != " ":
            return False
        self.board[row][col] = piece
        return True

    def unplace(self, row, col):
        self.board[row][col] = " "

    def test_match(self, pieces):
        if " " in pieces:
            return False

        q_match = sum([int(x.q) for x in pieces])
        if q_match == 4 or q_match == 0:
            print("QMATCH")
            return True

        overline_match = sum([int(x.overline) for x in pieces])
        if overline_match == 4 or overline_match == 0:
            print("OVL MATCH")
            return True

        underline_match = sum([int(x.underline) for x in pieces])
        if underline_match == 4 or underline_match == 0:
            print("UND MATCH")
            return True

        uppercase_match = sum([int(x.uppercase) for x in pieces])
        if uppercase_match == 4 or uppercase_match == 0:
            print("CASE MATCH")
            return True

        return False

    # todo: test_match can be rewritten so that only this is
    # necessary
    def get_coord_lanes(self):
        lanes = []

        # horizontal
        for i in range(len(self.board)):
            cells = []
            for j in range(len(self.board[i])):
                cells.append((i,j))
            lanes.append(cells)

        # vertical
        for i in range(len(self.board[0])):
            cells = []
            for j in range(len(self.board)):
                cells.append((j,i))
            lanes.append(cells)

        # diagonal 
            lanes.append([
                (0,0), (1,1), (2,2), (3,3)
            ])

            lanes.append([
                (0,3), (1,2), (2,1), (3,0)
            ])

        return lanes
    def get_lanes(self):
        lanes = []

        # horizontal
        lanes += self.board 

        # vertical
        for i in range(len(self.board[0])):
            cells = []
            for j in range(len(self.board)):
                cells.append(self.board[j][i])
            lanes.append(cells)

        # diagonal 
            lanes.append([
                self.board[0][0],
                self.board[1][1],
                self.board[2][2],
                self.board[3][3],
            ])

            lanes.append([
                self.board[0][3],
                self.board[1][2],
                self.board[2][1],
                self.board[3][0],
            ])

        return lanes

    def check_win(self):
        for lane in self.get_lanes():
            if self.test_match(lane):
                return True
        return False

    def check_draw(self):
        return len(self.valid_cells()) == 0
