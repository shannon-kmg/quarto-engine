import numpy as np
from Piece import Piece
from Board import Board
from PlayerConsole import PlayerConsole
from PlayerRandom import PlayerRandom
from PlayerHeuristic import PlayerHeuristic

def play_game():
    b = Board()
    q = PlayerRandom(True)
    g = PlayerHeuristic(False, q)
    b.draw()
    while True:
        # Q turn
        if len(b.valid_cells()) == 0:
            print("Draw!")
            return
        q.move(b, g.select_opponent_piece(q))
        b.draw()
        print("Q has moved.")
        if b.check_win():
            print("Q won!")
            return
        # G turn
        if len(b.valid_cells()) == 0:
            print("Draw!")
            return
        g.move(b, q.select_opponent_piece(g))
        b.draw()
        print("G has moved.")
        if b.check_win():
            print("G won!")
            return


play_game()
