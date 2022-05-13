from othello import Othello

if __name__ == "__main__":
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

        board.makeMove(x, y)

    res = board.computeScore()

    if res == 0:
        print("Tie")
    elif res == 1:
        print("Black Win")
    else:
        print("White Win")
