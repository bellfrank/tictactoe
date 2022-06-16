from flask import Flask, render_template, session, redirect, url_for
# flask sessions to give everyone a different game
from flask_session import Session
from tempfile import mkdtemp
import math
from helpers import apology

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

X = "X"
O = "O"
Empty = None


@app.route("/")
def index():
    return render_template("index.html")

# TIC TAC TOE

@app.route("/tictactoe")
def tictactoe():
    # store our board in a session
    if "board" not in session:
        session["board"] = [[Empty, Empty, Empty],
                            [Empty, Empty, Empty],
                            [Empty, Empty, Empty]]
        session["turn"] = X
        session["counter"] = 0

    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):

    # Storing user choice to board
    session["board"][row][col] = session["turn"]

    # must check rows
    winner = check_winner(session["board"])
    
    # if no more plays left
    if winner == Empty:
        return render_template("game.html", tie=True)

    # if there's a winner
    if winner:
        return render_template("game.html", winner=True, turn=session["turn"])

    # increment counter
    session["counter"] += 1

    # switching user
    if session["turn"] == X:
        session["turn"] = O
    else:
        session["turn"] = X

    return redirect(url_for("tictactoe"))


@app.route("/help")
def help():
    print(session["board"], session["turn"])
    step = minimax(session["board"], session["turn"])
    return redirect(url_for("play", row=1, col=1))


@app.route("/reset")
def reset():
    session["board"] = [[Empty, Empty, Empty],
                        [Empty, Empty, Empty],
                        [Empty, Empty, Empty]]
    session["turn"] = X
    session["counter"] = 0

    return redirect(url_for("tictactoe"))


def check_winner(board):

    # checks to see if user wins by a row
    row1 = board[0][0] == board[0][1] == board[0][2] != Empty
    row2 = board[1][0] == board[1][1] == board[1][2] != Empty
    row3 = board[2][0] == board[2][1] == board[2][2] != Empty

    if row1 or row2 or row3:
        return True

    # checks to see if user wins by a columns
    col1 = board[0][0] == board[1][0] == board[2][0] != Empty
    col2 = board[0][1] == board[1][1] == board[2][1] != Empty
    col3 = board[0][2] == board[1][2] == board[2][2] != Empty

    if col1 or col2 or col3:
        return True

    # checks to see if user wins by diagonals
    dia1 = board[0][0] == board[1][1] == board[2][2] != Empty
    dia2 = board[2][0] == board[1][1] == board[0][2] != Empty

    if dia1 or dia2:
        return True

    # checks to see if there are still plays remaining
    for i in range(3):
        for j in range(3):
            if board[i][j] == Empty:
                return False
        
    # If no plays remaining, return None
    return None

step = list()
def minimax(game, turn):
    global step

    # if game is over, return score for game ( BASE CONDITION )
    winner = check_winner(game)

    # X is the winner return 1
    if winner and turn == O:
        return 1
    # 0 is the winner return -1 
    if winner and turn == X:
        return -1
    # if winner == None:
    #     return 0
    
    # available moves
    moves = list()

    for i in range(len(game)):
        for j in range(len(game)):
            if (game[i][j] == Empty):
                moves.append([i, j])
    
    print("available moves", moves)
    print("whose turn", turn)

    if turn == X:
        value = -math.inf
        for move in moves:
            x, y = move
            game[x][y] = X
            print(game)
            result = max(value, minimax(game, O))
            if (value < result):
                value = result
                step.append([x,y])
                print(step)

    else:
        value = math.inf
        for move in moves:
            x, y = move
            game[x][y] = O
            result = max(value, minimax(game, X))
            if (value > result):
                value = result
                step.append([x,y])
    
    print(step)
    return step


# Connect4
@app.route("/connect4")
def connect4():
    
    return render_template("connect4.html")

@app.route("/resetconnect4")
def resetconnect4():
    pass

# DRAW
@app.route("/draw")
def draw():
    return render_template("draw.html")


# QUIZ
@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

# CARDS
@app.route("/flashcards")
def flashcards():
    return render_template("flashcards.html")



if __name__ == "__main__":
    app.run()


# list comprehension example
# ls = [[1,2],[3,4],[5,6]]
# >>> x = 7
# >>> [(i, e.index(x)) for i, e in enumerate(ls) if x in e]