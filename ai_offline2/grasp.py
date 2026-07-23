import algorithms

def grasp_maxcut(graph, max_iterations=50, alpha=0.5, seed=None):
    best_in_x = None
    best_weight = -1
    weight_per_iteration = []

    for i in range(max_iterations):
        run_seed = None
        if seed is not None:
            run_seed = seed + i

        constructed = algorithms.semi_greedy_maxcut(graph, alpha, run_seed)
        improved = algorithms.local_search(graph, constructed)
        weight = algorithms.cut_weight(graph, improved)

        weight_per_iteration.append(weight)

        if weight > best_weight:
            best_weight = weight
            best_in_x = improved

    return best_in_x, best_weight, weight_per_iteration
