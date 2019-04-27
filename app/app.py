import base64
import random

from flask import Flask, jsonify, make_response, request, render_template, redirect

from socialchoice import Election
from socialchoice.viz import write_beatgraph

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

pairs = {frozenset((x, y)) for x in candidates for y in candidates if x != y}


@app.route("/")
def index():
    seen_cookie = request.cookies.get("seen")
    seen_pairs = {frozenset(x.split(",")) for x in seen_cookie.split("\n")} if seen_cookie else set()

    if set(seen_pairs) == set(pairs):
        return render_template("done.html")
    else:
        possible_pairs = list(pairs.difference(seen_pairs))
        c1, c2 = possible_pairs[random.randint(0, len(possible_pairs) - 1)]

        resp = make_response(render_template("index.html", c1=c1, c2=c2, seen=seen_pairs))
        seen_pairs.add((c1, c2))
        resp.set_cookie('seen', "\n".join([",".join(pair) for pair in seen_pairs]))
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
    election = Election()
    election.add_votes(*votes)
    victory_graph = election.get_victory_graph()
    rankings = election.get_ranked_pairs_ranking()

    win_ratios = {x: y for x, y in election.win_ratio()}

    image_data = base64.b64encode(write_beatgraph(victory_graph, rankings, win_ratios)).decode("utf8")

    return f"""
    <body><h2>Current Matchups:</h4><img src="data:image/png;base64,{image_data}"/></body>
    """


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
