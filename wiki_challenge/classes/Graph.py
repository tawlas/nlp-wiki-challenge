# *********************** Graph class *********************************
class Graph:
    """ Adjacency map-based graph implementation """

    # *********************** Vertex class *********************************
    class Vertex:
        """Lightweight vertex structure for a graph."""
        __slots__ = '_element'

        def __init__(self, x):
            """Do not call constructor directly. Use Graph s insert vertex(x)."""
            self._element = x

        def element(self):
            """Return element associated with this vertex."""
            return self._element

        def __hash__(self):  # will allow vertex to be a map/set key
            return hash(id(self))

    # *********************** Edge Class *********************************
    class Edge:
        """Lightweight edge structure for a graph."""
        __slots__ = '_origin', '_destination', '_element'

        def __init__(self, u, v, x):
            """Do not call constructor directly. Use Graph s insert edge(u,v,x)."""
            self._origin = u
            self._destination = v
            self._element = x

        def endpoints(self):
            """Return (u,v) tuple for vertices u and v."""
            return (self._origin, self._destination)

        def opposite(self, v):
            """Return the vertex that is opposite v on this edge."""
            return self._destination if v is self._origin else self._origin

        def element(self):
            """Return element associated with this edge."""
            return self._element

        def __hash__(self):  # will allow edge to be a map/set key
            return hash((self._origin, self._destination))

    # *********************** Graph class methods *********************************
    def __init__(self, articles, connectivity_threshold=20, unique=True, directed=False):
        """Create an empty graph (undirected, by default).

        Graph is directed if optional paramter is set to True.
        """
        self._outgoing = {}
        # only create second map for directed graph; use alias for undirected
        self._incoming = {} if directed else self._outgoing
        self._connectivity_threshold = connectivity_threshold
        self._unique = unique
        self.initilialize_graph(articles)

    def do_share_n_unique_tokens(self, article_1, article_2):
        """ Check whether two articles share a number of unique tokens greater than the connectivity threshold value """
        common_tokens = set(article_1['tokens_count'].keys()).intersection(
            article_2['tokens_count'].keys())
        n_common_tokens = len(common_tokens)
        if n_common_tokens >= self._connectivity_threshold:
            return n_common_tokens
        else:
            return 0

    def do_share_n_token_instances(self, article_1, article_2):
        """ Check whether two articles share a number of token instances greater than the connectivity threshold value """

        common_tokens = set(article_1['tokens_count'].keys()).intersection(
            article_2['tokens_count'].keys())
        n_token_instances_1 = sum(
            [article_1['tokens_count'][token] for token in common_tokens])
        n_token_instances_2 = sum(
            [article_2['tokens_count'][token] for token in common_tokens])
        n_common_token_instances = min(
            n_token_instances_1, n_token_instances_2)
        if n_common_token_instances > self._connectivity_threshold:
            return n_common_token_instances
        else:
            return 0

    def initilialize_graph(self, articles):
        """ Build the graph. Add all the articles vertices and connect them. """
        for article in articles:
            self.insert_vertex(article)

        adjacency_map = self.build_adjacency_map()  # main bottleneck
        for u in adjacency_map:
            for v, n_common_words in adjacency_map[u]:
                self.insert_edge(u, v, n_common_words)

    def build_adjacency_map(self):
        """ Build the adjacency map of the graph. """
        adjacency_map = {}
        vertices = self.vertices()
        for u in vertices:
            article_1 = u.element()
            title_1 = article_1['title']
            adjacency_map[u] = set()
            for v in vertices:
                article_2 = v.element()
                title_2 = article_2['title']
                if self._unique:
                    n_common_words = self.do_share_n_unique_tokens(
                        article_1, article_2)
                else:
                    n_common_words = self.do_share_n_token_instances(
                        article_1, article_2)
                if title_1 != title_2 and n_common_words:
                    adjacency_map[u].add((v, n_common_words))

        return adjacency_map

    def is_directed(self):
        """Return True if this is a directed graph; False if undirected.

        Property is based on the original declaration of the graph, not its contents.
        """
        return self._incoming is not self._outgoing  # directed if maps are distinct

    def vertex_count(self):
        """Return the number of vertices in the graph."""
        return len(self._outgoing)

    def vertices(self):
        """Return an iteration of all vertices of the graph."""
        return self._outgoing.keys()

    def edge_count(self):
        """Return the number of edges in the graph."""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # for undirected graphs, make sure not to double-count edges
        return total if self.is_directed() else total // 2

    def edges(self):
        """Return a set of all edges of the graph."""
        result = set()  # avoid double-reporting edges of undirected graph
        for secondary_map in self._outgoing.values():
            # add edges to resulting set
            result.update(secondary_map.values())
        return result

    def get_edge(self, u, v):
        """Return the edge from u to v, or None if not adjacent."""
        return self._outgoing[u].get(v)  # returns None if v not adjacent

    def degree(self, v, outgoing=True):
        """Return number of (outgoing) edges incident to vertex v in the graph.

        If graph is directed, optional parameter used to count incoming edges.
        """
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """Return all (outgoing) edges incident to vertex v in the graph.

        If graph is directed, optional parameter used to request incoming edges.
        """
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None):
        """Insert and return a new Vertex with element x."""
        v = self.Vertex(x)
        self._outgoing[v] = {}
        if self.is_directed():
            # need distinct map for incoming edges
            self._incoming[v] = {}
        return v

    def insert_edge(self, u, v, x=None):
        """Insert and return a new Edge from u to v with auxiliary element x."""
        e = self.Edge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
