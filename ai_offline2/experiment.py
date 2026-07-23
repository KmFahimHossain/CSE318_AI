import os
import csv
import time

import graph
import algorithms
import grasp

# known best solutions / upper bounds
KNOWN_BEST = {
    "g1": 12078, "g2": 12084, "g3": 12077,
    "g11": 627, "g12": 621, "g13": 645,
    "g14": 3187, "g15": 3169, "g16": 3172,
    "g22": 14123, "g23": 14129, "g24": 14131,
    "g32": 1560, "g33": 1537, "g34": 1541,
    "g35": 8000, "g36": 7996, "g37": 8009,
    "g43": 7027, "g44": 7022, "g45": 7020,
    "g48": 6000, "g49": 6000, "g50": 5988,
}

def make_graph_name(filename):
    # turn "g2.rud" into "G2"
    digits = ""
    for ch in filename:
        if ch.isdigit():
            digits = digits + ch
    if digits == "":
        return os.path.splitext(filename)[0]
    return "G" + digits

def extract_number(filename):
    digits = ""
    for ch in filename:
        if ch.isdigit():
            digits = digits + ch
    if digits == "":
        return 0
    return int(digits)

def run_one_graph(filepath, alpha=0.5, num_runs=10, grasp_iterations=50, seed=1):
    g = graph.load_graph(filepath)

    randomized_avg = algorithms.randomized_maxcut(g, 30, seed)

    greedy_solution = algorithms.greedy_maxcut(g)
    greedy_weight = algorithms.cut_weight(g, greedy_solution)

    # run semi-greedy construction and randomized-start local search several times to get best/avg
    semi_greedy_weights = []
    local_search_weights = []

    for i in range(num_runs):
        run_seed = seed + i
        constructed = algorithms.semi_greedy_maxcut(g, alpha, run_seed)
        semi_greedy_weights.append(algorithms.cut_weight(g, constructed))

        randomized_start = algorithms.randomized_solution(g, run_seed)
        improved = algorithms.local_search(g, randomized_start)
        local_search_weights.append(algorithms.cut_weight(g, improved))

    semi_greedy_avg = sum(semi_greedy_weights) / len(semi_greedy_weights)

    local_search_best = local_search_weights[0]
    for w in local_search_weights:
        if w > local_search_best:
            local_search_best = w
    local_search_avg = sum(local_search_weights) / len(local_search_weights)

    best_x, grasp_best, grasp_history = grasp.grasp_maxcut(g, grasp_iterations, alpha, seed)
    grasp_avg = sum(grasp_history) / len(grasp_history)

    row = {
        "Name": make_graph_name(os.path.basename(filepath)),
        "V": g.num_vertices,
        "E": len(g.edges),
        "Randomized-1": round(randomized_avg, 2),
        "Simple-Greedy": greedy_weight,
        "Semi-Greedy-1 (alpha={})".format(alpha): round(semi_greedy_avg, 2),
        "Local-Search (best)": local_search_best,
        "Local-Search (avg)": round(local_search_avg, 2),
        "GRASP (best)": grasp_best,
        "GRASP (avg)": round(grasp_avg, 2),
        "GRASP (# iterations)": grasp_iterations,
        "Known-Best": "",
    }

    key = row["Name"].lower()
    if key in KNOWN_BEST:
        row["Known-Best"] = KNOWN_BEST[key]

    return row

def run_all(graph_folder, output_csv, alpha=0.5, num_runs=10, grasp_iterations=50):
    filenames = os.listdir(graph_folder)
    graph_files = filenames
    graph_files.sort(key=extract_number)

    total = len(graph_files)
    if total == 0:
        print("no graph files found in", graph_folder)
        return
    print("found", total, "graph files in", graph_folder)

    out_file = open(output_csv, "w", newline="")
    writer = None

    for i in range(total):
        filename = graph_files[i]
        filepath = os.path.join(graph_folder, filename)

        print("[" + str(i + 1) + "/" + str(total) + "] running " + filename + " ...", end=" ", flush=True)

        start_time = time.time()
        row = run_one_graph(filepath, alpha, num_runs, grasp_iterations)
        elapsed = time.time() - start_time

        print("done in {:.1f}s".format(elapsed),
              "| greedy =", row["Simple-Greedy"],
              "| grasp best =", row["GRASP (best)"],
              "| known best =", row["Known-Best"])

        if writer is None:
            fieldnames = list(row.keys())
            writer = csv.DictWriter(out_file, fieldnames=fieldnames)
            writer.writeheader()

        writer.writerow(row)
        out_file.flush()

    out_file.close()
    print("")
    print("all", total, "graphs done, results written to", output_csv)

if __name__ == "__main__":
    run_all("dataset/graph_GRASP/set1", "2205090.csv")
