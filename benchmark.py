from othello import Othello
from MCTS import MCTS
from random import choice
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import numpy as np
import matplotlib

matplotlib.use("agg")
import matplotlib.pyplot as plt


TEST_AMOUNT = 100
NUM_ITERATIONS = [5, 10, 25, 50, 75, 100]


def mcts_move(board, num_iterations):
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
        # smaller distance, higher probs
        dist = min(x, abs(borderline_dist - x)) + \
            min(y, abs(borderline_dist - y))
        dist = board.n - dist
        return dist

    dist_vals = [computeDistance(x) for x in valid_moves]

    denom = sum(dist_vals)
    probs = [num / denom for num in dist_vals]

    psdrdm_move_idx = np.random.choice(np.arange(len(valid_moves)), p=probs)
    psdrdm_move = valid_moves[psdrdm_move_idx]
    return board.makeMove(psdrdm_move[0], psdrdm_move[1])


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


def job(color, num_iterations, player):
    win_count = 0
    for _ in tqdm(range(TEST_AMOUNT)):
        win_count += run(color, num_iterations, player)
    
    return win_count / TEST_AMOUNT

if __name__ == "__main__":

    results = {}

    color_map = {"black_random": '#26580f', 'black_pseudorandom': "#378805",
                 'white_random': '#072f5f', 'white_pseudorandom': '#1261a0'}


    pool = Pool(processes=4)

    for color in ["black", "white"]:
        for player in ["random", "pseudorandom"]:
            print(color, player)
            res = pool.starmap(job, [(color, num_iterations, player) for num_iterations in NUM_ITERATIONS])
            print(res)
            plt.plot(
                NUM_ITERATIONS, res, label=f"mcts-agent as {color} against {player}", c=color_map[f'{color}_{player}'])

    plt.ylabel("Win Rate(%)")
    plt.xlabel("Num Iterations")
    plt.title("MCTS-Othello Benchmark")
    plt.legend()
    plt.savefig("benchmark.png")
