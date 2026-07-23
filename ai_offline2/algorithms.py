import random

def cut_weight(graph, in_x):
    # in_x is a list of booleans, in_x[v] = True means vertex v is in partition X
    total = 0
    for edge in graph.edges:
        u = edge[0]
        v = edge[1]
        w = edge[2]
        if in_x[u] != in_x[v]: # Crossing edge
            total = total + w
    return total

def randomized_solution(graph, seed=None):
    rng = random.Random(seed)
    in_x = [False] * (graph.num_vertices + 1)

    for v in range(1, graph.num_vertices + 1):
        in_x[v] = rng.random() >= 0.5
    return in_x

def randomized_maxcut(graph, num_runs=30, seed=None):
    rng = random.Random(seed)
    total_weight = 0

    for run in range(num_runs):
        in_x = randomized_solution(graph, rng.randrange(10**9))
        total_weight = total_weight + cut_weight(graph, in_x)
    average_weight = total_weight / num_runs
    return average_weight


def greedy_maxcut(graph):
    n = graph.num_vertices
 
    # find the edge with maximum weight
    best_edge = graph.edges[0]
    for edge in graph.edges:
        if edge[2] > best_edge[2]:
            best_edge = edge
    u0 = best_edge[0]
    v0 = best_edge[1]
 
    in_x = [False] * (n + 1)
    assigned = [False] * (n + 1)
 
    in_x[u0] = True
    assigned[u0] = True
    in_x[v0] = False
    assigned[v0] = True
 
    # sigma_x[z] = sum of weights from z to vertices currently in X
    # sigma_y[z] = sum of weights from z to vertices currently in Y
    sigma_x = [0] * (n + 1)
    sigma_y = [0] * (n + 1)
 
    for neighbor in graph.adj[u0]:
        sigma_x[neighbor] = sigma_x[neighbor] + graph.adj[u0][neighbor]
    for neighbor in graph.adj[v0]:
        sigma_y[neighbor] = sigma_y[neighbor] + graph.adj[v0][neighbor]
 
    for z in range(1, n + 1):
        if assigned[z]:
            continue
 
        if sigma_y[z] > sigma_x[z]:
            in_x[z] = True
            assigned[z] = True
            for neighbor in graph.adj[z]:
                sigma_x[neighbor] = sigma_x[neighbor] + graph.adj[z][neighbor]
        else:
            in_x[z] = False
            assigned[z] = True
            for neighbor in graph.adj[z]:
                sigma_y[neighbor] = sigma_y[neighbor] + graph.adj[z][neighbor]
 
    return in_x


def semi_greedy_maxcut(graph, alpha=0.5, seed=None):
    rng = random.Random(seed)
    n = graph.num_vertices
 
    # start the same way greedy
    best_edge = graph.edges[0]
    for edge in graph.edges:
        if edge[2] > best_edge[2]:
            best_edge = edge
    u0 = best_edge[0]
    v0 = best_edge[1]
 
    in_x = [False] * (n + 1)
    assigned = [False] * (n + 1)
 
    in_x[u0] = True
    assigned[u0] = True
    in_x[v0] = False
    assigned[v0] = True
 
    sigma_x = [0] * (n + 1)
    sigma_y = [0] * (n + 1)
 
    for neighbor in graph.adj[u0]:
        sigma_x[neighbor] = sigma_x[neighbor] + graph.adj[u0][neighbor]
    for neighbor in graph.adj[v0]:
        sigma_y[neighbor] = sigma_y[neighbor] + graph.adj[v0][neighbor]
 
    remaining = []
    for v in range(1, n + 1):
        if not assigned[v]:
            remaining.append(v)
 
    while len(remaining) > 0:
        # greedy function value for each candidate: max(sigma_x[v], sigma_y[v])
        values = []
        for v in remaining:
            value = sigma_x[v]
            if sigma_y[v] > value:
                value = sigma_y[v]
            values.append(value)
 
        w_min = values[0]
        w_max = values[0]
        for value in values:
            if value < w_min:
                w_min = value
            if value > w_max:
                w_max = value
        mu = w_min + alpha * (w_max - w_min)
 
        rcl = []
        for i in range(len(remaining)):
            if values[i] >= mu:
                rcl.append(remaining[i])
 
        chosen = rcl[rng.randrange(len(rcl))]
 
        # same rule as greedy: z goes to whichever side its other-side sum is larger
        if sigma_y[chosen] > sigma_x[chosen]:
            in_x[chosen] = True
            assigned[chosen] = True
            for neighbor in graph.adj[chosen]:
                sigma_x[neighbor] = sigma_x[neighbor] + graph.adj[chosen][neighbor]
        else:
            in_x[chosen] = False
            assigned[chosen] = True
            for neighbor in graph.adj[chosen]:
                sigma_y[neighbor] = sigma_y[neighbor] + graph.adj[chosen][neighbor]
 
        remaining.remove(chosen)
 
    return in_x


def local_search(graph, in_x):
    n = graph.num_vertices
    in_x = list(in_x)  # work on a copy

    # sigma_x[v] = sum of weights from v to current members of X
    # sigma_y[v] = sum of weights from v to current members of Y
    sigma_x = [0] * (n + 1)
    sigma_y = [0] * (n + 1)

    for v in range(1, n + 1):
        for neighbor in graph.adj[v]:
            w = graph.adj[v][neighbor]
            if in_x[neighbor]:
                sigma_x[v] = sigma_x[v] + w
            else:
                sigma_y[v] = sigma_y[v] + w

    improved = True
    while improved:
        improved = False
        best_vertex = -1
        best_delta = 0

        for v in range(1, n + 1):
            if in_x[v]:
                delta = sigma_x[v] - sigma_y[v]
            else:
                delta = sigma_y[v] - sigma_x[v]

            if delta > best_delta:
                best_delta = delta
                best_vertex = v

        if best_vertex != -1:
            improved = True
            # flip the partition of best_vertex and update sigma values of its neighbors
            moving_to_x = not in_x[best_vertex]
            for neighbor in graph.adj[best_vertex]:
                w = graph.adj[best_vertex][neighbor]
                if moving_to_x:
                    sigma_x[neighbor] = sigma_x[neighbor] + w
                    sigma_y[neighbor] = sigma_y[neighbor] - w
                else:
                    sigma_x[neighbor] = sigma_x[neighbor] - w
                    sigma_y[neighbor] = sigma_y[neighbor] + w
            in_x[best_vertex] = moving_to_x

    return in_x
