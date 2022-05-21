from othello import Othello
from MCTS import MCTS
from random import choice


TEST_AMOUNT = 100
NUM_ITERATIONS = [5, 20, 50, 100]


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


# if mcts wins return True
def run(mcts_agent, num_iterations):
    board = Othello(8)
    while True:
        if mcts_agent == "black":
            if board.is_terminal():
                break
            board = mcts_move(board, num_iterations)

            if board.is_terminal():
                break
            board = random_move(board)

        elif mcts_agent == "white":
            if board.is_terminal():
                break
            board = random_move(board)

            if board.is_terminal():
                break
            board = mcts_move(board, num_iterations)

    winner_map = {1: "black", 0: "white"}
    res = board.computeScore()
    return winner_map[res] == mcts_agent


if __name__ == "__main__":

    results = {}

    for color in ["black", "white"]:
        for num_iterations in NUM_ITERATIONS:
            win_count = 0
            for _ in range(TEST_AMOUNT):
                win_count += run(color, num_iterations)

            results[(color, num_iterations)] = results

    with open('results.txt', 'w', encoding='utf-8') as f:
        f.write(str(results))
