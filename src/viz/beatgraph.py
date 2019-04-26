import networkx as nx
from collections import defaultdict


def write_beatgraph(victory_graph: nx.DiGraph, rankings: list, output_filename: str):
    """Draws the beatgraph of the given matchups to a file

    :param victory_graph: a nx_graph, with nodes as candidates and edges (u, v)
    representing a victory where u beat v. Each edge must have the edge_data attribute
    "margin", explaining by how much u beat v.
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

        # print(u, v, list(paths), len(list(paths)))
        if not has_other_path:
            new_graph.add_edge(u, v)

    new_graph.remove_edges_from(to_remove)

    import pygraphviz as pgv

    G = pgv.AGraph(directed=True)
    G.node_attr['style'] = 'filled'

    base_color = "0.000 0.000 "
    for n in victory_graph.nodes:
        color = .5 - rankings.index(n) / len(rankings) / 3
        G.add_node(n, fillcolor=base_color + ("%.30f" % color))

    for u, v in new_graph.edges:
        G.add_edge(u, v, new_graph.get_edge_data(u, v))

    G.layout(prog='dot')
    G.draw(output_filename)


if __name__ == '__main__':
    g = nx.DiGraph()
    g.add_node("python")
    g.add_node("java")
    g.add_node("scala")

    g.add_edge("python", "java", margin=30)
    g.add_edge("scala", "java", margin=60)
    g.add_edge("scala", "python", margin=10)

    rankings = ["scala", "python", "java"]

    output_filename = "viz.png"

    write_beatgraph(g, rankings, output_filename)
