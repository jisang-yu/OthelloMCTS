from othello import Othello
from MCTS import MCTS
from random import choice
import numpy as np


TEST_AMOUNT = 100
NUM_ITERATIONS = [5, 20, 50, 100]
PLAYER_AGENT = "pseudorandom"


def mcts_move(board, num_iterations):
    print(board)
    tree = MCTS()
    for _ in range(num_iterations):
        tree.do_rollout(board)

    return tree.choose(board)


def random_move(board):
    valid_moves = board.validMoves()
    move = choice(valid_moves)
    return board.makeMove(move[0], move[1])

def pseudorandom_move(board):
    valid_moves = board.validMoves()
    def computeDistance(coord):
        borderline_dist = board.n - 1
        x, y = coord[0], coord[1]
        dist = min(x, abs(borderline_dist - x)) + min(y, abs(borderline_dist - y)) # smaller distance, higher probs
        dist = board.n - dist
        return dist

    dist_vals = [computeDistance(x) for x in valid_moves]

    denom = sum(dist_vals)
    print(dist_vals)
    probs = [num / denom for num in dist_vals]

    psdrdm_move_idx = np.random.choice(np.arange(len(valid_moves)), p=probs)
    psdrdm_move = valid_moves[psdrdm_move_idx]
    return board.makeMove(psdrdm_move[0], psdrdm_move[1])

# if mcts wins return True
def run(mcts_agent, num_iterations, player_agent):
    board = Othello(8)
    while True:
        if mcts_agent == "black":
            if board.is_terminal():
                break
            board = mcts_move(board, num_iterations)

            if board.is_terminal():
                break

            if player_agent == "pseudorandom":
                board = pseudorandom_move(board)
            elif player_agent == "random":
                board = random_move(board)

        elif mcts_agent == "white":
            if board.is_terminal():
                break

            if player_agent == "pseudorandom":
                board = pseudorandom_move(board)
            elif player_agent == "random":
                board = random_move(board)

            if board.is_terminal():
                break
            board = mcts_move(board, num_iterations)

    winner_map = {1: "black", 0: "white", 0.5: "tie"}
    res = board.computeScore()
    return winner_map[res] == mcts_agent


if __name__ == "__main__":

    results = {}

    for color in ["black", "white"]:
        for num_iterations in NUM_ITERATIONS:
            win_count = 0
            for _ in range(TEST_AMOUNT):
                win_count += run(color, num_iterations, PLAYER_AGENT)

            results[(color, num_iterations)] = results

    with open('results.txt', 'w', encoding='utf-8') as f:
        f.write(str(results))
