import graph
import algorithms
import grasp

def print_partition(label, in_x, num_vertices):
    x_list = []
    y_list = []
    for v in range(1, num_vertices + 1):
        if in_x[v]:
            x_list.append(v)
        else:
            y_list.append(v)

    print(label)
    print("  X =", x_list)
    print("  Y =", y_list)

def main():
    g = graph.load_graph("input.txt")
    print("loaded graph with", g.num_vertices, "vertices and", len(g.edges), "edges")
    print("")

    # Randomized-1
    randomized_avg = algorithms.randomized_maxcut(g, 30, seed=1)
    print("Randomized (average over 30 runs):", randomized_avg)
    print("")

    # Greedy
    greedy_result = algorithms.greedy_maxcut(g)
    greedy_weight = algorithms.cut_weight(g, greedy_result)
    print_partition("Greedy", greedy_result, g.num_vertices)
    print("  weight =", greedy_weight)
    print("")

    # Semi-Greedy
    alpha = 0.5
    semi_greedy_result = algorithms.semi_greedy_maxcut(g, alpha, seed=1)
    semi_greedy_weight = algorithms.cut_weight(g, semi_greedy_result)
    print_partition("Semi-Greedy (alpha=" + str(alpha) + ")", semi_greedy_result, g.num_vertices)
    print("  weight =", semi_greedy_weight)
    print("")

    # Local Search starting from a randomized result
    randomized_result = algorithms.randomized_solution(g, seed=1)
    local_search_result = algorithms.local_search(g, randomized_result)
    local_search_weight = algorithms.cut_weight(g, local_search_result)
    print_partition("Local Search (from Randomized)", local_search_result, g.num_vertices)
    print("  weight =", local_search_weight)
    print("")

    # GRASP
    grasp_iterations = 50
    best_in_x, best_weight, history = grasp.grasp_maxcut(g, grasp_iterations, alpha, seed=1)
    print_partition("GRASP (best of " + str(grasp_iterations) + " iterations)", best_in_x, g.num_vertices)
    print("  weight =", best_weight)

if __name__ == "__main__":
    main()
