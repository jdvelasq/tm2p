def collect_node_degrees(nx_graph):

    degrees = []
    for node in nx_graph.nodes():
        degrees.append((node, nx_graph.nodes[node]["degree"]))
    degrees = sorted(degrees, key=lambda x: x[1], reverse=True)

    return degrees
