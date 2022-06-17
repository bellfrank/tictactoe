from flask import Flask, render_template, session, redirect, url_for, request
# flask sessions to give everyone a different game
from flask_session import Session
from tempfile import mkdtemp
import math
import datetime
import requests
from helpers import apology, numcheck

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# This creates an issue with my heroku application
# app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

X = "X"
O = "O"
Empty = None


@app.route("/")
def index():
    return render_template("index.html")

############################## TIC TAC TOE ############################## 

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
############################## END OF TIC TAC TOE ############################## 




############################## Mastergame ##############################

# Global Variables
API_CALL = False
numbers = []

@app.route("/mastergame")
def mastergame():

    if "combinations" not in session:
        session["combinations"] = []
    if "attempts" not in session:
        session["attempts"] = 10
    if "score" not in session:
        session["score"] = 0

    return render_template("mastergame.html",
        now = datetime.datetime.now(),
        combinations = session["combinations"],
        attempts = session["attempts"],
        score = session["score"]
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    # Global variables
    global API_CALL
    global numbers

    # Request 4 RANDOM integers from API (fetched once per game)
    if not API_CALL:
        response = requests.get('https://www.random.org/integers/?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new')
        numbers = response.text
        API_CALL = True

    # If user submits 4 digits
    if request.method == "POST":
        guess_counter = 0
       
        comb1 = int(request.form.get("number1"))
        comb2 = int(request.form.get("number2"))
        comb3 = int(request.form.get("number3"))
        comb4 = int(request.form.get("number4"))
        
        numbers_copy = []

        k = 0
        for num in numbers:
            if(num == '\n'):
                continue
            numbers_copy.append(int(num))
            k += 1


        # Backend 4 digit validation
        if not numcheck(comb1) or not numcheck(comb2) or not numcheck(comb3) or not numcheck(comb4):
            return render_template("mastergame.html",
            now = datetime.datetime.now(),
            message = "invalid input",
            combinations = session["combinations"],
            attempts = session["attempts"],
            score = session["score"]
        )
    
        # Checking user input against API number and generates feedback

        if comb1 == int(numbers[0]) and comb2 == int(numbers[2]) and comb3 == int(numbers[4]) and comb4 == int(numbers[6]):
            guess_message = "Well done! You guessed the correct number :)"
            session["score"] += 1
            session["attempts"] = 10
            session["combinations"] = []
            API_CALL = False
            
            return render_template("mastergame.html",
            now = datetime.datetime.now(),
            combinations = session["combinations"],
            attempts = session["attempts"],
            score = session["score"],
            guess_message = guess_message,
        )

        # N numbers correct and the right location
        flag1 = False
        flag2 = False
        flag3 = False
        flag4 = False

        if(comb1 == int(numbers[0])):
            guess_counter += 1
            flag1 = True
        if(comb2 == int(numbers[2])):
            guess_counter +=1
            flag2 = True
        if(comb3 == int(numbers[4])):
            guess_counter += 1
            flag3 = True
        if(comb4 == int(numbers[6])):
            guess_counter += 1
            flag4 = True
        
        
        # If you guessed correct numbers but in the wrong location
        # searching the list and if the user's input is in the list
        guess_counter2 = 0
        
        if not flag1 and comb1 in numbers_copy:
            guess_counter2 += 1
        if not flag2 and comb2 in numbers_copy:
            guess_counter2 += 1
        if not flag3 and comb3 in numbers_copy:
            guess_counter2 += 1
        if not flag4 and comb4 in numbers_copy:
            guess_counter2 += 1
        

        guess_message = f"You have guessed {guess_counter} numbers correctly and their right location! :)" + f"You also guessed {guess_counter2} numbers correctly but not in their right location!"

        if guess_counter == 0 and guess_counter2 == 0:
            guess_message = "Your guess was incorrect :("

        # Add user guess to history of guesses
        session["combinations"] += [f"{comb1}  {comb2}  {comb3}  {comb4} - {guess_message}"]
        session["attempts"] -= 1

        
        return render_template("mastergame.html",
            now = datetime.datetime.now(),
            combinations = session["combinations"],
            attemps = session["attempts"],
            score = session["score"],
            guess_message = guess_message,
        )
    
    else:
        return redirect(url_for("mastergame"))

@app.route("/resetmastergame", methods=["POST"])
def resetmastergame():
    # resets number by allowing API to get called again, once
    global API_CALL
    API_CALL = False
    
    session["combinations"] = []
    session["attempts"] = 10
    session["score"] = 0
    
    return redirect(url_for("mastergame"))






############################## END OF MASTERGAME ##############################

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