# Quarto

A console implementation of [Quarto](https://en.wikipedia.org/wiki/Quarto_(board_game)).

---

## Installation

```bash
git clone <repo-url>
cd quarto
python3 game.py
```

By default, the game runs against the heuristic engine. To run the heuristic engine against a random player instead, replace `PlayerConsole` with `PlayerRandom` in `game.py`.

---

## Gameplay

Each turn, the current player receives a piece selected by the opponent and places it on any empty cell. A player wins by completing a row of four pieces (horizontal, vertical, or diagonal) that all share at least one attribute.

**The four attributes:**

| Attribute | Values |
|-----------|--------|
| Letter | `Q` or `G` |
| Case | uppercase or lowercase |
| Top marking | line on top, no line on top |
| Bottom marking | line on bottom, no line on bottom |

After placing a piece, the player selects a piece for the opponent to place on their next turn. The game ends when a player completes a winning row, or all cells are filled with no winner.

---

## Heuristic engine

The engine evaluates every legal move using two signals: **danger** and **move score**.

### Danger

Each piece in the opponent's hand is assigned a danger value representing how likely it is to complete a winning row.

For each potential win lane (row, column, or diagonal), a piece's danger value increases if it shares a trait with all pieces already in that lane. The increase is proportional to the number of pieces already in the lane. If placing the piece in a lane would instead result in a win for the engine, the danger value is decreased.

The engine selects the piece with the lowest danger value to give to the opponent.

### Move score

Each candidate move is scored based on how it affects winning opportunities for both players. For each lane affected by a move:

- The score **increases** if the move creates a winning opportunity for the engine.
- The score **decreases** if it creates a winning opportunity for the opponent.

The magnitude of the change scales with the number of pieces already in the affected lane.

**Example:** Placing a `q` piece into a lane that already contains two `q` pieces, when the opponent holds a `q` piece, gives the opponent a one-move win. That move receives a large negative score.

### Final move selection

The engine selects the move with the highest combined score:

```
final score = move score + danger delta
```

where *danger delta* is the change in the danger rating of the opponent's least dangerous piece after the move is made. The implementation is located in `HeuristicEngine.py`.
