import random
from pathlib import Path
from board import is_solvable
from heuristics import manhattan
from search import solve

DEFAULT_OUTPUT_FILE = "puzzle.txt"
DEFAULT_PUZZLE_COUNT = 10
DEFAULT_SIZE = 4
DEFAULT_TIME_LIMIT = 25.0

def generate_candidate(k):
    values = list(range(k * k))
    while True:
        random.shuffle(values)
        board = tuple(values)
        if is_solvable(board, k):
            return board

def append_puzzle(file_handle, k, board):
    file_handle.write(f"{k}\n")
    for row in range(k):
        start = row * k
        end = start + k
        file_handle.write(" ".join(str(value) for value in board[start:end]) + "\n")
    file_handle.write("\n")

def generate_puzzles(output_file=DEFAULT_OUTPUT_FILE, puzzle_count=DEFAULT_PUZZLE_COUNT, k=DEFAULT_SIZE, time_limit=DEFAULT_TIME_LIMIT):
    output_path = Path(output_file)
    accepted = 0

    with output_path.open("w") as file_handle:
        attempt = 0
        while accepted < puzzle_count:
            attempt += 1
            board = generate_candidate(k)
            print(
                f"Attempt {attempt} going on...",
                flush=True,
            )
            path, cost, nodes_expanded = solve(board, k, manhattan, weight=1.0, time_limit=time_limit)
            if cost < 0 or path is None:
                continue

            append_puzzle(file_handle, k, board)
            accepted += 1
            print(
                f"Accepted puzzle {accepted}/{puzzle_count} on attempt {attempt} "
                f"(cost={cost}, nodes={nodes_expanded})",
                flush=True,
            )

if __name__ == "__main__":
    generate_puzzles()
