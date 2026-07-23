import csv
import random

def read_rows(csv_path):
    rows = []
    file = open(csv_path, "r")
    reader = csv.DictReader(file)
    for row in reader:
        rows.append(row)
    file.close()
    return rows

def get_semi_greedy_key(row):
    for key in row:
        if key.startswith("Semi-Greedy"):
            return key
    return None

def write_report(csv_path, output_path="report.txt", num_graphs=5, seed=None):
    rows = read_rows(csv_path)

    known_rows = []
    for row in rows:
        if row["Known-Best"] != "":
            known_rows.append(row)

    if len(known_rows) == 0:
        print("no rows with a known best value found in", csv_path)
        return

    rng = random.Random(seed)
    if num_graphs >= len(known_rows):
        sample = known_rows
    else:
        sample = rng.sample(known_rows, num_graphs)

    semi_greedy_key = get_semi_greedy_key(sample[0])

    out = open(output_path, "w")

    out.write("MAX-CUT results - raw values\n\n")

    values_header = "{:<8}{:>10}{:>10}{:>10}{:>10}{:>14}{:>12}{:>13}{:>14}\n".format(
        "Graph", "KnownBest", "Random", "Greedy", "SemiGry", "LocalSrch", "GRASPbst", "GRASPavg", "Avg/Best")
    out.write(values_header)

    for row in sample:
        name = row["Name"]
        known_best = float(row["Known-Best"])
        randomized = float(row["Randomized-1"])
        greedy = float(row["Simple-Greedy"])
        semi_greedy = float(row[semi_greedy_key])
        local_search = float(row["Local-Search (best)"])
        grasp_best = float(row["GRASP (best)"])
        grasp_avg = float(row["GRASP (avg)"])
        avg_best_ratio = grasp_avg / grasp_best

        line = "{:<8}{:>10.0f}{:>10.1f}{:>10.1f}{:>10.1f}{:>14.1f}{:>12.1f}{:>13.1f}{:>14.3f}\n".format(
            name, known_best, randomized, greedy, semi_greedy, local_search, grasp_best, grasp_avg, avg_best_ratio)
        out.write(line)

    out.write("\n")
    out.write("MAX-CUT results, scaled to known best (1.0 = matches known best)\n\n")

    header = "{:<8}{:>10}{:>10}{:>10}{:>10}{:>14}{:>12}{:>13}{:>14}\n".format(
        "Graph", "KnownBest", "Random", "Greedy", "SemiGry", "LocalSrch", "GRASPbst", "GRASPavg", "Avg/Best")
    out.write(header)

    for row in sample:
        name = row["Name"]
        known_best = float(row["Known-Best"])
        randomized = float(row["Randomized-1"]) / known_best
        greedy = float(row["Simple-Greedy"]) / known_best
        semi_greedy = float(row[semi_greedy_key]) / known_best
        local_search = float(row["Local-Search (best)"]) / known_best
        grasp_best_raw = float(row["GRASP (best)"])
        grasp_avg_raw = float(row["GRASP (avg)"])
        grasp_best = grasp_best_raw / known_best
        grasp_avg = grasp_avg_raw / known_best
        avg_best_ratio = grasp_avg_raw / grasp_best_raw

        line = "{:<8}{:>10.0f}{:>10.3f}{:>10.3f}{:>10.3f}{:>14.3f}{:>12.3f}{:>13.3f}{:>14.3f}\n".format(
            name, known_best, randomized, greedy, semi_greedy, local_search, grasp_best, grasp_avg, avg_best_ratio)
        out.write(line)

    out.close()
    print("wrote", output_path)

if __name__ == "__main__":
    write_report("2205090.csv", "report.txt", 5)
