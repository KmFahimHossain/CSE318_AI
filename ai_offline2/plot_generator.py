import os
import csv
import matplotlib.pyplot as plt

def read_results(csv_path):
    names = []
    randomized = []
    greedy = []
    semi_greedy = []
    local_search_best = []
    grasp_best = []
    grasp_avg = []
    known_best = []

    file = open(csv_path, "r")
    reader = csv.DictReader(file)

    for row in reader:
        names.append(row["Name"])
        randomized.append(float(row["Randomized-1"]))
        greedy.append(float(row["Simple-Greedy"]))
        local_search_best.append(float(row["Local-Search (best)"]))
        grasp_best.append(float(row["GRASP (best)"]))
        grasp_avg.append(float(row["GRASP (avg)"]))

        semi_greedy_value = None
        for key in row:
            if key.startswith("Semi-Greedy"):
                semi_greedy_value = float(row[key])
        semi_greedy.append(semi_greedy_value)

        if row["Known-Best"] == "":
            known_best.append(None)
        else:
            known_best.append(float(row["Known-Best"]))

    file.close()

    results = {
        "names": names,
        "randomized": randomized,
        "greedy": greedy,
        "semi_greedy": semi_greedy,
        "local_search_best": local_search_best,
        "grasp_best": grasp_best,
        "grasp_avg": grasp_avg,
        "known_best": known_best,
    }
    return results

def split_into_batches(results, batch_size):
    total = len(results["names"])
    batches = []

    start = 0
    while start < total:
        end = start + batch_size
        if end > total:
            end = total

        batch = {
            "names": results["names"][start:end],
            "randomized": results["randomized"][start:end],
            "greedy": results["greedy"][start:end],
            "semi_greedy": results["semi_greedy"][start:end],
            "local_search_best": results["local_search_best"][start:end],
            "grasp_best": results["grasp_best"][start:end],
            "grasp_avg": results["grasp_avg"][start:end],
            "known_best": results["known_best"][start:end],
        }
        batches.append(batch)
        start = end

    return batches

def batch_label(batch):
    first_name = batch["names"][0]
    last_name = batch["names"][len(batch["names"]) - 1]
    return first_name + "-" + last_name

def plot_algorithm_comparison(batch, output_path):
    names = batch["names"]
    x_positions = range(len(names))
    width = 0.15

    plt.figure(figsize=(12, 5))
    plt.bar([p - 2 * width for p in x_positions], batch["randomized"], width, label="Randomized")
    plt.bar([p - width for p in x_positions], batch["greedy"], width, label="Greedy")
    plt.bar(x_positions, batch["semi_greedy"], width, label="Semi-Greedy")
    plt.bar([p + width for p in x_positions], batch["local_search_best"], width, label="Local Search")
    plt.bar([p + 2 * width for p in x_positions], batch["grasp_best"], width, label="GRASP")

    plt.xticks(list(x_positions), names, rotation=90)
    plt.ylabel("Cut weight")
    plt.title("Algorithm comparison: " + batch_label(batch))
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.gca().set_axisbelow(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print("saved", output_path)

def plot_grasp_best_vs_avg(batch, output_path):
    names = batch["names"]
    x_positions = range(len(names))
    width = 0.35

    plt.figure(figsize=(12, 5))
    plt.bar([p - width / 2 for p in x_positions], batch["grasp_best"], width, label="GRASP best")
    plt.bar([p + width / 2 for p in x_positions], batch["grasp_avg"], width, label="GRASP avg")

    plt.xticks(list(x_positions), names, rotation=90)
    plt.ylabel("Cut weight")
    plt.title("GRASP best vs average: " + batch_label(batch))
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.gca().set_axisbelow(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print("saved", output_path)

def plot_ratio_to_known_best(batch, output_path):
    names = []
    greedy_ratio = []
    semi_greedy_ratio = []
    local_search_ratio = []
    grasp_ratio = []

    total = len(batch["names"])
    for i in range(total):
        if batch["known_best"][i] is None:
            continue

        best = batch["known_best"][i]
        names.append(batch["names"][i])
        greedy_ratio.append(batch["greedy"][i] / best)
        semi_greedy_ratio.append(batch["semi_greedy"][i] / best)
        local_search_ratio.append(batch["local_search_best"][i] / best)
        grasp_ratio.append(batch["grasp_best"][i] / best)

    if len(names) == 0:
        print("no graphs with a known best value in this batch, skipping ratio plot for", output_path)
        return

    x_positions = range(len(names))
    width = 0.2

    plt.figure(figsize=(12, 5))
    plt.bar([p - 1.5 * width for p in x_positions], greedy_ratio, width, label="Greedy")
    plt.bar([p - 0.5 * width for p in x_positions], semi_greedy_ratio, width, label="Semi-Greedy")
    plt.bar([p + 0.5 * width for p in x_positions], local_search_ratio, width, label="Local Search")
    plt.bar([p + 1.5 * width for p in x_positions], grasp_ratio, width, label="GRASP")

    plt.axhline(y=1.0, linestyle="--")
    plt.xticks(list(x_positions), names, rotation=90)
    plt.ylabel("Ratio to known best solution")
    plt.title("Ratio to known best: " + batch_label(batch))
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.gca().set_axisbelow(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print("saved", output_path)

def generate_all_plots(csv_path, output_folder="plots", batch_size=10):
    results = read_results(csv_path)
    batches = split_into_batches(results, batch_size)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # one all-in-one chart per task, covering every graph in the CSV
    all_comparison_path = os.path.join(output_folder, "algorithm_comparison_all.png")
    plot_algorithm_comparison(results, all_comparison_path)

    all_grasp_path = os.path.join(output_folder, "grasp_best_vs_avg_all.png")
    plot_grasp_best_vs_avg(results, all_grasp_path)

    all_ratio_path = os.path.join(output_folder, "ratio_to_known_best_all.png")
    plot_ratio_to_known_best(results, all_ratio_path)

    # per-batch charts, 10 graphs at a time, so each chart stays readable
    for batch in batches:
        label = batch_label(batch)

        comparison_path = os.path.join(output_folder, "algorithm_comparison_" + label + ".png")
        plot_algorithm_comparison(batch, comparison_path)

        grasp_path = os.path.join(output_folder, "grasp_best_vs_avg_" + label + ".png")
        plot_grasp_best_vs_avg(batch, grasp_path)

        ratio_path = os.path.join(output_folder, "ratio_to_known_best_" + label + ".png")
        plot_ratio_to_known_best(batch, ratio_path)

if __name__ == "__main__":
    generate_all_plots("2205090.csv")
