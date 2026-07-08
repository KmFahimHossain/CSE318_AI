from pathlib import Path
from search import solve
from heuristics import manhattan

PUZZLE_FILE = "puzzle.txt"

def read_puzzles(file_path=PUZZLE_FILE):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Puzzle file not found: {file_path}")

    with path.open("r") as f:
        data = f.read().split()

    puzzles = []
    idx = 0
    while idx < len(data):
        k = int(data[idx])
        idx += 1

        values = []
        for _ in range(k * k):
            values.append(int(data[idx]))
            idx += 1
        puzzles.append((k, tuple(values)))

    return puzzles


def run_experiment(file_path=PUZZLE_FILE):
    weights = [1.0, 1.2, 2.0, 5.0]

    puzzles = read_puzzles(file_path)

    rows = []
    for i in range(len(puzzles)):
        k, puzzle = puzzles[i]
        for w in weights:
            path, cost, nodes_expanded = solve(puzzle, k, manhattan, w)

            row = {}
            row["puzzle_id"] = i + 1
            row["heuristic"] = "manhattan"
            row["weight"] = w
            row["cost"] = cost
            row["nodes_expanded"] = nodes_expanded
            rows.append(row)

            status = "solved" if cost >= 0 else "stopped"
            print(
                f"Puzzle {i + 1}, weight {w}: {status} "
                f"(cost={cost}, nodes={nodes_expanded})",
                flush=True,
            )

    return rows

if __name__ == "__main__":
    rows = run_experiment()
    for row in rows:
        print(row)
