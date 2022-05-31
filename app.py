from flask import Flask, render_template, session, redirect, url_for
# flask sessions to give everyone a different game
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    #store our board in a session
    if "board" not in session:
        session["board"] = [[None, None, None],[None, None, None], [None, None, None]]
        session["turn"] = "X"
    
    return render_template("game.html", game=session["board"], turn=session["turn"])



@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    
    return redirect(url_for("index"))