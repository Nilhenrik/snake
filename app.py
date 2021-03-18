from flask import Flask, render_template, request
from board import Board
import json
import numpy

app = Flask(__name__, template_folder=".")

# counter = 0
# board = numpy.zeros((20,20), dtype=bool)

game = Board()
game_gen = game.game()

#board = Board()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/next")
def next_state():
    p1 = request.args.get("p1")
    p2 = request.args.get("p2")
    print(p1, p2)
    if p1 == "-2" and p2 == "-2":
        game.restart()
        p1 = "-1"
        p2 = "-1"
    # global counter
    # x = counter % 20
    # y = counter // 20
    # board[x,y] = not board[x,y]
    # counter += 1
    # if counter == 400:
    #     counter -= 400
    while True:
        try:
            state_obj = {"board": next(game.gen).tolist()}
            break
        except StopIteration:
            game.restart()
    return json.dumps(state_obj)