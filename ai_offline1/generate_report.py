import csv
from experiment import run_experiment

def write_report(rows, filename="report.csv"):
    fieldnames = ["puzzle_id", "heuristic", "weight", "cost", "nodes_expanded"]
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            output_row = dict(row)
            output_row.setdefault("heuristic", "manhattan")
            writer.writerow(output_row)

if __name__ == "__main__":
    rows = run_experiment()
    write_report(rows)
