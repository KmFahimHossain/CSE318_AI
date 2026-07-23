class Graph:
    def __init__(self, num_vertices, edges):
        self.num_vertices = num_vertices
        self.edges = edges  # list of (u, v, w)

        # adjacency list : adj[v] is a dict {neighbor1 : weight1, neighbor2 : weight2}
        self.adj = []
        for i in range(num_vertices + 1):
            self.adj.append({})

        for edge in edges:
            u = edge[0]
            v = edge[1]
            w = edge[2]
            self.adj[u][v] = w
            self.adj[v][u] = w

def load_graph(filepath):
    file = open(filepath, "r")
    lines = file.readlines()
    file.close()

    first_line = lines[0].split()
    n = int(first_line[0])
    m = int(first_line[1])

    edges = []
    for i in range(1, m + 1):
        parts = lines[i].split()
        u = int(parts[0])
        v = int(parts[1])
        w = int(parts[2])
        edges.append((u, v, w))

    graph = Graph(n, edges)
    return graph
