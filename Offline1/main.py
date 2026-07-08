import sys
from board import is_solvable, print_board
from search import solve
from heuristics import HEURISTICS

def read_input(file_path="input.txt"):
    with open(file_path, "r") as f:
        data = f.read().split()
    idx = 0
    k = int(data[idx])
    idx = idx + 1

    values = []
    for i in range(k * k):
        values.append(int(data[idx]))
        idx = idx + 1

    board = tuple(values)
    return k, board

def main():
    input_file = "input.txt"
    if len(sys.argv) > 3:
        input_file = sys.argv[3]

    k, board = read_input(input_file)

    h_name = "manhattan"
    if len(sys.argv) > 1:
        h_name = sys.argv[1]

    weight = 1.0
    if len(sys.argv) > 2:
        weight = float(sys.argv[2])

    h_func = HEURISTICS[h_name]

    if is_solvable(board, k) == False:
        print("Unsolvable puzzle")
        return

    path, cost, nodes_expanded = solve(board, k, h_func, weight)
    
    print("Minimum number of moves = " + str(cost) + "\n")
    for i, b in enumerate(path):
        print(print_board(b, k))
        if i < len(path) - 1:
            print()

if __name__ == "__main__":
    main()
