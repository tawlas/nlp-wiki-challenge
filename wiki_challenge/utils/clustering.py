def DFS(g, u, discovered, cluster):
    """Perform DFS of the undiscovered portion of Graph g starting at Vertex u.
    discovered is a dictionary mapping each vertex to the edge that was used to
    discover it during the DFS. (u should be ”discovered” prior to the call.)
    Newly discovered vertices will be added to the dictionary as a result.

    :param g: a Graph class object
    :type g: Graph
    :param u: a Vertex object from which to discover adjacent nodes.
    :type u: Graph.Vertex
    :param discovered: a dict of discovered nodes. A key in that dict is a
    discovered node and the corresponding value is the tree edge that discovered v
    :type discovered: dict
    :param cluster: A list of nodes belonging in the same cluster.
    :type cluster: list
    """
    for e in g.incident_edges(u):  # for every outgoing edge from u
        v = e.opposite(u)
        if v not in discovered:  # v is an unvisited vertex
            discovered[v] = e  # e is the tree edge that discovered v
            cluster.append(v)
            DFS(g, v, discovered, cluster)  # recursively explore from v


def DFS_complete(g):
    """Perform DFS for entire graph and return forest as a dictionary.

    forest maps each vertex v to the edge that was used to discover it.
    (Vertices that are roots of a DFS tree are mapped to None.)

    :param g: a Graph class object
    :type g: Graph
    :return: A tuple of dicts summarizing the clusters of the input graph. The second returned value, 
    that which is of interest in this project, is a dict where a key is a discovery vertex of a cluster
    and its corresponding value is the list of vertices in its cluster.
    :rtype: tuple
    """
    forest = {}
    clusters = {}
    for u in g.vertices():
        if u not in forest:
            forest[u] = None  # u will be the root of a tree
            cluster = [u]
            DFS(g, u, forest, cluster)
            clusters[u] = cluster
    return forest, clusters
