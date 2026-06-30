# Quarto

A console implementation of the game [Quarto](https://en.wikipedia.org/wiki/Quarto_(board_game))

## Installation and setup
- clone the repository
- run `python3 game.py`
- this will put you up against a heuristic based engine

- alternatively, you can change PlayerConsole to PlayerRandom in game.py, and
  see the heuristic algorithm compete against a player placing pieces randomly

## Playing
- Each time it is your turn, you will be given a piece selected by the other
  player, which you can place anywhere on the board
- If you place 4 pieces in a row that share some attribute, you win the game
- The attributes are:
    - Q or G
    - uppercase or lowercase
    - line on top or no line on top
    - line on bottom or no line on botton
- After you have placed a piece, you can choose a piece for your opponent to
  place. Be careful not to hand them a victory!
- The game continues until someone wins or all squares on the board have been
  filled

## Explanation
### Heuristic algorithm
- The AI for this game uses a heuristic algorithm to calculate 1. the optimal
  cell in which to place the piece it has been given and 2. the optimal piece
to give to its opponent.
- The code for the heuristic calculations is located in HeuristicEngine.py
#### Dangers
- Each piece in the opponent's hand is given a 'danger' rating based on how
  advantageous it is to the opponent.
- The AI will always attemt to give its opponent the least dangerous piece it
  can
- Danger calculations are done when evaluating the board state. For each
  potential win lane (e.g. vertical, horizontal, diagonal), we increase the
danger value of an opponent piece if it shares one or more traits with all the
pieces in that lane. The more pieces in the lane, the more the danger value is
increased. If placing a piece in the lane could potentially grant the
AI a win, the danger value for this piece is decreased.
#### Move Score
- Each potential move is assigned a move score, the move score is a rating of
  how advantageous a move is to the player vs the opponent. Essentially, for
each lane a move affects, the move score increases if te move creates a winning
opportunity for the player, and decreases if it creates a winning opportunity
for the opponent. The amount the move score increases or decreases by is based
on the the number of pieces remaining in the affected lanes.

- For example: If our move is to place a `q` piece in a lane that already has 2
  `q` pieces, and the opponent has a `q` piece, this gives the opponent a win
opporunity in 1 move, so this move will be assigned a high negative score.
#### Move calculation
- The heuristic algorithm checks each possible move in a given position, and
  assigns it a score. The move with the highes score is the one that is
selected.
- The score assigned to a particular move is the sum of the move score, and the
  danger delta, where the danger delta is the increase or decrease in the
danger value of the least dangerous piece held by the opponent.
