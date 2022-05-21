from othello import Othello
from collections import namedtuple
from random import choice
from MCTS import MCTS, Node

if __name__ == "__main__":
    tree = MCTS()
    board = Othello(4)

    while True:
        print(board)
        valids = board.validMoves()
        print(valids)

        if len(valids) == 0:
            break

        print("Select your move in x,y form: ")
        move = input()
        move = move.split(",")

        if len(move) != 2:
            continue

        x, y = int(move[0]), int(move[1])

        board = board.makeMove(x, y)

        # Here, we train as we go, doing fifty rollouts each turn.
        for _ in range(50):
            tree.do_rollout(board)
        board = tree.choose(board)
        print(board.to_pretty_string())
        if board.terminal:
            break

    res = board.computeScore()

    if res == 0:
        print("Tie")
    elif res == 1:
        print("Black Win")
    else:
        print("White Win")
