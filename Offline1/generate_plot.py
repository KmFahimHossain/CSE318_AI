import csv
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPORT_FILE = "report.csv"
PLOTS_DIR = "plots"

def read_report(filename=REPORT_FILE):
    with open(filename, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            rows.append(
                {
                    "puzzle_id": int(row["puzzle_id"]),
                    "heuristic": row.get("heuristic", "manhattan"),
                    "weight": float(row["weight"]),
                    "cost": float(row["cost"]),
                    "nodes_expanded": float(row["nodes_expanded"]),
                }
            )
    return rows

def _aggregate_by_heuristic_and_weight(rows, value_key):
    grouped = defaultdict(list)
    for row in rows:
        heuristic = row.get("heuristic", "manhattan")
        grouped[(heuristic, row["weight"])].append(row[value_key])

    summary = defaultdict(list)
    for (heuristic, weight), values in grouped.items():
        summary[heuristic].append((weight, sum(values) / len(values)))

    for heuristic in summary:
        summary[heuristic].sort(key=lambda item: item[0])

    return summary

def _group_rows_by_weight(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["weight"]].append(row)
    return dict(sorted(grouped.items(), key=lambda item: item[0]))

def _group_rows_by_puzzle(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["puzzle_id"]].append(row)
    for puzzle_id in grouped:
        grouped[puzzle_id].sort(key=lambda row: row["weight"])
    return dict(sorted(grouped.items(), key=lambda item: item[0]))

def _plot_metric_by_puzzle(rows, value_key, title, ylabel, output_file):
    grouped = _group_rows_by_puzzle(rows)
    weights = sorted({row["weight"] for row in rows})

    plt.figure(figsize=(10, 6))
    cmap = plt.get_cmap("tab20")
    for index, (puzzle_id, puzzle_rows) in enumerate(grouped.items()):
        puzzle_rows = sorted(puzzle_rows, key=lambda row: row["weight"])
        x_values = [row["weight"] for row in puzzle_rows]
        y_values = [row[value_key] for row in puzzle_rows]
        color = cmap(index % cmap.N)
        plt.plot(
            x_values,
            y_values,
            marker="o",
            linewidth=1.5,
            alpha=0.75,
            color=color,
            label=f"Puzzle {puzzle_id}",
        )

    summary = _aggregate_by_heuristic_and_weight(rows, value_key)
    for heuristic, points in summary.items():
        weights_summary = [weight for weight, _ in points]
        values_summary = [value for _, value in points]
        plt.plot(
            weights_summary,
            values_summary,
            color="black",
            linewidth=3,
            marker="s",
            markersize=6,
            label=f"Average ({heuristic})",
        )

    plt.title(title)
    plt.xlabel("Weight")
    plt.ylabel(ylabel)
    plt.xticks(weights)
    plt.grid(True, alpha=0.3)
    plt.legend(ncol=2, fontsize=8, frameon=False)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def write_charts(rows, output_dir=PLOTS_DIR):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    _plot_metric_by_puzzle(
        rows,
        "nodes_expanded",
        "Nodes Expanded by Puzzle and Weight",
        "Nodes Expanded",
        output_path / "report_nodes_expanded.png",
    )
    _plot_metric_by_puzzle(
        rows,
        "cost",
        "Solution Cost by Puzzle and Weight",
        "Solution Cost",
        output_path / "report_cost.png",
    )

if __name__ == "__main__":
    rows = read_report()
    write_charts(rows)
