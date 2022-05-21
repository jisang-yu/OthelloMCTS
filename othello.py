import copy
from collections import namedtuple
from random import choice
from MCTS import MCTS, Node

class Othello:
    def __init__(self, n=8):
        # O indicates black and X indicates white
        # Othello board is an nxn board where n is even and n > 2
        if n % 2 != 0:
            return None
        self.n = n
        self.board = [["." for _ in range(n)] for _ in range(n)]

        # Initialize 4 middle stones
        self.board[n//2-1][n//2-1], self.board[n//2][n//2] = "X", "X"
        self.board[n//2][n//2-1], self.board[n//2-1][n//2] = "O", "O"

        self.black_count, self.white_count = 2, 2

        self.current_player = "O"

    def find_children(self):
        self.is_leaf = True
        if not self.validMoves:
            self.is_leaf = False

        if self.is_leaf: # If the game is finished then no moves can be made
            return set()

        # Otherwise, you can make a move in each of the empty spots
        return {self.makeMove(i) for i, value in enumerate(self.tup) if value is None}

    def find_random_child(self):
        if board.terminal:
            return None  # If the game is finished then no moves can be made
        empty_spots = [i for i, value in enumerate(board.tup) if value is None]
        return self.makeMove(choice(empty_spots))


    def validMoves(self) -> list[tuple[int]]:
        """
        Looking at the current board and player, find the next valid moves
        :return: list[tuple[int]], list of valid moves, where move is (x,y)
        """
        res = []
        for check_x in range(self.n):
            for check_y in range(self.n):
                if self.board[check_x][check_y] != ".":
                    continue

                direction = [(1, 0), (1, 1), (0, 1), (0, -1),
                             (-1, -1), (-1, 0), (1, -1), (-1, 1)]

                for dx, dy in direction:
                    if self.__canFlip(check_x, check_y, dx, dy):
                        res.append((check_x, check_y))
                        break

        return res

    def makeMove(self, x: int, y: int):
        """
        creates a new Othello instance with the new move. If move is invalid, return None
        :param x, y: x and y coordinate of the move to make
        :return: new Othello instance with new move
        """
        if not (0 <= x < self.n and 0 <= y < self.n):
            print("Error: Invalid Move")
            return

        if self.board[x][y] != ".":
            print("Error: Board position already taken")
            return

        new_board = copy.deepcopy(self)

        opponent = "O" if self.current_player == "X" else "X"
        player_is_black = True if self.current_player == "O" else False

        new_board.board[x][y] = self.current_player
        if player_is_black:
            self.black_count += 1
        else:
            self.white_count += 1

        direction = [(1, 0), (1, 1), (0, 1), (0, -1),
                     (-1, -1), (-1, 0), (1, -1), (-1, 1)]

        for dx, dy in direction:

            # check if we can flip in this direction
            if not self.__canFlip(x, y, dx, dy):
                continue

            # flip correct amount of stones in this direction
            temp_x, temp_y = x + dx, y + dy
            while 0 <= temp_x < self.n and 0 <= temp_y < self.n and self.board[temp_x][temp_y] == opponent:
                new_board.board[temp_x][temp_y] = self.current_player
                new_board.black_count += 1 if player_is_black else -1
                new_board.white_count += -1 if player_is_black else 1
                temp_x += dx
                temp_y += dy

        # reverse turn
        new_board.current_player = opponent
        return new_board

    def computeScore(self):
        if self.black_count == self.white_count:
            return 0.5

        return 1 if self.black_count > self.white_count else 0

    def __canFlip(self, x, y, dx, dy) -> bool:
        '''
            Private Method
            Look at current position of the board and checks if we can flip stones in the direction provided
        '''
        lst = []
        temp_x, temp_y = x + dx, y + dy
        while 0 <= temp_x < self.n and 0 <= temp_y < self.n:
            lst.append(self.board[temp_x][temp_y])
            temp_x += dx
            temp_y += dy

        opponent = "O" if self.current_player == "X" else "X"

        if self.current_player not in lst:
            return False
        else:
            first_player = lst.index(self.current_player)

        if "." not in lst:
            first_empty = float("inf")
        else:
            first_empty = lst.index(".")

        if opponent not in lst:
            return False
        else:
            first_opponent = lst.index(opponent)

        # empty is in between
        if first_empty < first_player:
            return False

        # no stones to flip
        if first_player < first_opponent:
            return False

        return True

    def __str__(self):
        res = ""
        for i in range(self.n):
            for j in range(self.n):
                res += f" {self.board[i][j]} "

            res += "\n"

        res += f"Black: {self.black_count}, White: {self.white_count}"

        return res

    def __hash__(self):
        return hash(self.board)

    def __eq__(node1, node2):
        return node1.board == node2.board
