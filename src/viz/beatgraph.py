import math

import networkx as nx
import pygraphviz as pgv


def write_beatgraph(victory_graph: nx.DiGraph, rankings: list, win_ratio: dict, output_filename: str = ""):
    """Draws the beatgraph of the given matchups to a file

    :param victory_graph: a nx_graph, with nodes as candidates and edges (u, v)
    representing a victory where u beat v. Each edge must have the edge_data attribute
    "margin", explaining by how much u beat v.
    :param win_ratio: a dictionary mapping node names to win ratios in [0, 1]
    :param rankings: an array, with the same elements as `nx_graph.nodes`, with the ranking of the nodes.
    :param output_filename: the name of the file to write to
    """
    win_edges = sorted([edge for edge in victory_graph.edges],
                       key=lambda x: victory_graph.get_edge_data(x[0], x[1])["margin"],
                       reverse=True)

    new_graph = nx.DiGraph()
    new_graph.add_nodes_from(victory_graph.nodes)
    for (u, v) in win_edges:
        if v not in nx.descendants(new_graph, u):
            new_graph.add_edge(u, v)

    to_remove = []
    e = [x for x in new_graph.edges]
    for (u, v) in e:
        new_graph.remove_edge(u, v)
        has_other_path = nx.has_path(new_graph, u, v)

        if not has_other_path:
            new_graph.add_edge(u, v)

    new_graph.remove_edges_from(to_remove)

    G = pgv.AGraph(directed=True)
    G.node_attr['style'] = 'filled'

    base_color = "0.520 0.500 "
    for n in victory_graph.nodes:
        color = 1 - rankings.index(n) / len(rankings) / 2
        G.add_node(n, fillcolor=base_color + ("%.3f" % color),
                   height=math.sqrt(win_ratio[n]) * 2,
                   width=math.sqrt(win_ratio[n]) * 2)

    for u, v in new_graph.edges:
        edge_data = victory_graph.get_edge_data(u, v)
        G.add_edge(u, v, penwidth=math.sqrt(edge_data["margin"] / 4),
                   xlabel="%.2f" % (edge_data["margin"] / 100),
                   labelfloat="false")

    G.layout(prog='dot')
    if output_filename:
        G.draw(output_filename, format="png")
    else:
        return G.draw(format="png", prog="dot")


if __name__ == '__main__':
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

    output_filename = "viz.png"

    write_beatgraph(g, rankings, win_ratios, output_filename)
