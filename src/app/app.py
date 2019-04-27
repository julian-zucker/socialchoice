import base64
import datetime
import random

import networkx as nx
from flask import Flask, jsonify, make_response, request, render_template, redirect

from src.viz.beatgraph import write_beatgraph

app = Flask(__name__)

votes = []
candidates = [
    "scala",
    "python",
    "rust",
    "golang",
    "java",
    "C",
    "C++",
]

@app.route("/")
def index():
    seen = (request.cookies.get("seen") or "").split(",")

    c1 = None
    while not c1:
        choice = candidates[random.randint(0, len(candidates)-1)]
        if choice not in seen:
            c1 = choice

    c2 = None
    while not c2:
        choice = candidates[random.randint(0, len(candidates)-1)]
        if choice not in seen and choice != c1:
            c2 = choice

    resp = make_response(render_template("index.html", c1=c1, c2=c2))
    resp.set_cookie('seen', f"{seen},{c1},{c2}")
    return resp

@app.route("/vote/<c1>/<c2>/<result>")
def vote(c1, c2, result):
    votes.append([c1, c2, result])
    return redirect("/")

@app.route("/get_votes")
def get_votes():
    return jsonify(votes)


@app.route("/view_results/")
def view_results():
    g = nx.DiGraph()
    g.add_node("python")
    g.add_node("java")
    g.add_node("scala")
    g.add_node("fortran")
    g.add_node("cobol")

    g.add_edge("scala", "java", margin=60)
    g.add_edge("scala", "python", margin=10)
    g.add_edge("scala", "cobol", margin=12)
    g.add_edge("scala", "fortran", margin=100)

    g.add_edge("python", "java", margin=30)
    g.add_edge("python", "cobol", margin=20)
    g.add_edge("python", "fortran", margin=80)

    g.add_edge("java", "cobol", margin=80)
    g.add_edge("java", "c", margin=23)

    g.add_edge("c", "cobol", margin=80)

    g.add_edge("fortran", "cobol", margin=10)

    rankings = ["scala", "python", "java", "c", "fortran", "cobol"]

    win_ratios = {
        "scala": 1,
        "python": .8,
        "java": .6,
        "c": .4,
        "fortran": .2,
        "cobol": .1,
    }

    image_data = base64.b64encode(write_beatgraph(g, rankings, win_ratios)).decode("utf8")

    return f"""
    <body><h2>Current Matchups:</h4><img src="data:image/png;base64,{image_data}"/></body>
    """


if __name__ == '__main__':
    app.run()
