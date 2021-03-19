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
    else:
        
    #if p1 != "-1":
        #game.snakes[0].dir = #int(p1)
        #game.snakes[1].dir = #(2 + int(p1)) % 4
        for snake in game.snakes:
            n_dir = next(snake.ai.gen)
            if n_dir != -1:
                snake.dir = n_dir#next(snake.ai.gen)
        p1 = "-1"
    #if p2 != "-1":
    #    game.snakes[1].dir = int(p2)
    #    p1 = "-1"
    while True:
        try:
            state_obj = {
                "board": next(game.gen).tolist(),
                "player1": [game.snakes[0].x, game.snakes[0].y],
                "player2": [game.snakes[1].x, game.snakes[1].y],
                "message": game.message,
                }
            game.message = ""
            break
        except StopIteration:
            game.restart()
    return json.dumps(state_obj)