from typing import Tuple, Dict

def _goal_positions(k: int) -> Dict[int, Tuple[int, int]]:
    positions = {}
    for i in range(k * k):
        val = (i + 1) % (k * k)  # last cell wraps to 0 (blank)
        row = i // k
        col = i % k
        positions[val] = (row, col)
    return positions

def hamming(board: Tuple[int, ...], k: int, goal_pos=None) -> int:
    goal_pos = goal_pos or _goal_positions(k)
    count = 0
    for i in range(len(board)):
        val = board[i]
        if val == 0:
            continue
        row = i // k
        col = i % k
        if (row, col) != goal_pos[val]:
            count += 1
    return count


def manhattan(board: Tuple[int, ...], k: int, goal_pos=None) -> int:
    goal_pos = goal_pos or _goal_positions(k)
    total = 0
    for i in range(len(board)):
        val = board[i]
        if val == 0:
            continue
        row = i // k
        col = i % k
        grow, gcol = goal_pos[val]
        total += abs(row - grow) + abs(col - gcol)
    return total


def euclidean(board: Tuple[int, ...], k: int, goal_pos=None) -> float:
    goal_pos = goal_pos or _goal_positions(k)
    total = 0.0
    for i in range(len(board)):
        val = board[i]
        if val == 0:
            continue
        row = i // k
        col = i % k
        grow, gcol = goal_pos[val]
        total += ((row - grow) ** 2 + (col - gcol) ** 2) ** 0.5
    return total


def linear_conflict(board: Tuple[int, ...], k: int, goal_pos=None) -> int:
    goal_pos = goal_pos or _goal_positions(k)
    base = manhattan(board, k, goal_pos)
    conflicts = 0

    # row conflicts
    for row in range(k):
        line = []
        for col in range(k):
            val = board[row * k + col]
            if val != 0 and goal_pos[val][0] == row:
                line.append((col, goal_pos[val][1]))
        for a in range(len(line)):
            for b in range(a + 1, len(line)):
                cur_a, goal_a = line[a]
                cur_b, goal_b = line[b]
                if cur_a < cur_b and goal_a > goal_b:
                    conflicts += 1
                elif cur_a > cur_b and goal_a < goal_b:
                    conflicts += 1

    # column conflicts
    for col in range(k):
        line = []
        for row in range(k):
            val = board[row * k + col]
            if val != 0 and goal_pos[val][1] == col:
                line.append((row, goal_pos[val][0]))
        for a in range(len(line)):
            for b in range(a + 1, len(line)):
                cur_a, goal_a = line[a]
                cur_b, goal_b = line[b]
                if cur_a < cur_b and goal_a > goal_b:
                    conflicts += 1
                elif cur_a > cur_b and goal_a < goal_b:
                    conflicts += 1

    return base + 2 * conflicts


def custom(board: Tuple[int, ...], k: int, goal_pos=None) -> int:
    """Basically king moves in chess - king can go diagonal so it's max(row_diff, col_diff), not sum.
    Manhattan is like a rook that can only go straight, so it adds row_diff + col_diff instead"""
    goal_pos = goal_pos or _goal_positions(k)
    total = 0
    for i in range(len(board)):
        val = board[i]
        if val == 0:
            continue
        row = i // k
        col = i % k
        grow, gcol = goal_pos[val]
        total += max(abs(row - grow), abs(col - gcol))
    return total


HEURISTICS = {
    "hamming": hamming,
    "manhattan": manhattan,
    "euclidean": euclidean,
    "linear_conflict": linear_conflict,
    "custom": custom,
}
