from abc import ABC, abstractmethod
from collections import defaultdict
import math

class Node(ABC):
    """
    A representation of a single Othello Gameboard state.
    MCTS works by constructing a tree of these Nodes.
    """

    @abstractmethod
    def find_children(self):
        "All possible successors of this board state"
        return set()

    @abstractmethod
    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        return None

    @abstractmethod
    def is_terminal(self):
        "Returns True if the node has no children"
        return True

    @abstractmethod
    def reward(self):
        "Assumes `self` is terminal node. 1=win, -1=loss, 0=tie, etc"
        return 0

    @abstractmethod
    def __hash__(self):
        "Nodes must be hashable"
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):
        "Nodes must be comparable"
        return True

class MCTS:
    """
    Monte Carlo Tree Searcher
    First we rollout the tree (select-expand-simulate-backpropagate)
    (for select, expand, simulate, backpropagate, refer to https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)
    Then we choose a move
    """

    def __init__(self, exploration_weight=1):
        self.Q = defaultdict(int) # total reward of each node
        self.N = defaultdict(int) # total visit count for each node
        self.children = dict() # children of each node
        self.exploration_weight = exploration_weight

    def choose(self, node):
        """
        Choose the best successor of node (i.e. Choose move in a game)
        :param node: class Node that represents current gameboard state
        :return: child node with maximum score
        """

        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal leaf node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf") # avoid unseen moves
            return self.Q[n] / self.N[n]

        return max(self.children[node], key=score)

    def do_rollout(self, node):
        """
        Make the tree one layer better. Train for one iteration
        :param node: class Node
        :return: None
        """
        path = self._select(node)

        # leaf is the final node of our recorded path
        leaf = path[-1]
        self._expand(leaf)

        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def _select(self, node):
        """
        Find an unexplored descendant of `node` by constructing the path
        :param node: class Node
        :return: path that is recorded until unexplored / leaf node
        """
        path = []

        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal(leaf)
                return path

            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path

            node = self._uct_select(node)

    def _expand(self, node):
        """
        Update the `children` dict with the child of the `node`
        :param node: class Node
        :return: only return when already expanded
        """
        if node in self.children:
            # already expanded, so return
            return

        self.children[node] = node.find_children()


    def _simulate(self, node):
        """
        Returns the reward for a random simulation (to completion) of `node`
        :param node: class Node
        :return: - reward / reward depending on result of simulation until completion
        """
        invert_reward = True
        while True:
            if node.is_terminal():
                reward = node.reward()
                return -reward if invert_reward else reward
            node = node.find_random_child()
            invert_reward = not invert_reward


    def _backpropagate(self, path, reward):
        """
        Send the reward back up to the ancestors of the leaf
        :param path: recorded path
        :param reward: reward earned from winning / losing the game
        :return: None
        """
        for node in reversed(path):
            # updates the nodes in recorded path
            self.N[node] += 1 # number of visits
            self.Q[node] += reward # reward
            reward = -reward  # 1 for me is -1 for my enemy, and vice versa


    def _uct_select(self, node):
        """
        Select a child of node, balancing exploration & exploitation
        :param node: class Node
        :return: given all child nodes, select the node with upper confidence bound
        """

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)

