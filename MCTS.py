from random import random
from othello import Othello


class Node:

    def __init__(self, state) -> None:

        self.state: Othello = state
        self.n_visit = 0
        self.n_wins = 0
        self.children: list[Node] = []

    def is_leaf():
        return True


class MCTS:
    def __init__(self):
        self.epsilon = 0.05
        self.tree = {}

    def exploreExploit(self, children: list[Node]):
        if len(children) == 0:
            return False

        return True if random() > self.epsilon else False

    def mcts(self, state: Node):

        select = self.exploreExploit(state.children)

        search_path = []
        for _ in range(num_iteration):

            elected_state = None
            while not selected_state.is_leaf():
                if select:  # we have children[]
                    # select child with most visits
                    selected_state = max(
                        state.children, key=lambda x: x.n_visits)
                else:
                    valids = state.valid_moves()
                    selected_ = random.choose(valids)

                    selected_state = Othello()  # create a new Othello instance with selected_

                    self.children.append(selected_state)

        for node in search_path:
            selected_state.computeScore()
