from flask import Flask, render_template, request
from board import Board
import json
import numpy

app = Flask(__name__, template_folder=".")

game = Board()
game_gen = game.game()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/next")
def next_state():
    p1 = request.args.get("p1")
    p2 = request.args.get("p2")
    if p1 == "-2" and p2 == "-2":
        game.restart()
        p1 = "-1"
        p2 = "-1"
    if p1 != "-1":
        game.snakes[0].dir = int(p1)
        p1 = "-1"
    if p2 != "-1":
        game.snakes[1].dir = int(p2)
        p1 = "-1"
    while True:
        try:
            state_obj = {"board": next(game.gen).tolist()}
            break
        except (StopIteration, RuntimeError):
            game.restart()
    return json.dumps(state_obj)