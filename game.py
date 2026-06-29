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
        q.move(b, g.select_opponent_piece(q))
        b.draw()
        print("Q has moved.")
        if b.check_win():
            print("Q won!")
            return
        # G turn
        g.move(b, q.select_opponent_piece(g))
        b.draw()
        print("G has moved.")
        if b.check_win():
            print("G won!")
            return


play_game()
