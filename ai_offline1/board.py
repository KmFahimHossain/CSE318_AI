from typing import Tuple, List

def goal_state(board, k):
    tiles = sorted(x for x in board if x > 0)

    goal = []
    idx = 0

    for cell in board:
        if cell == -1:
            goal.append(-1)
        else:
            if idx < len(tiles):
                goal.append(tiles[idx])
                idx += 1
            else:
                goal.append(0)

    return tuple(goal)

def blank_index(board: Tuple[int, ...]) -> int:
    return board.index(0)

def is_solvable(board: Tuple[int, ...], k: int) -> bool:
    seq = []
    for t in board:
        if t != 0 and t != -1:
            seq.append(t)

    # count inversions
    inversions = 0
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                inversions += 1

    if k % 2 == 1:
        # odd grid: solvable if and only if inversions is even
        return inversions % 2 == 0

    # even grid: depends on blank's row from bottom too
    blank_row_bottom = k - blank_index(board) // k
    if blank_row_bottom % 2 == 0:
        return inversions % 2 == 1
    else:
        return inversions % 2 == 0


def neighbors(board: Tuple[int, ...], k: int):
    idx = blank_index(board)
    row = idx // k
    col = idx % k

    candidate_moves = []

    if row > 0:
        candidate_moves.append(idx - k)
    if row < k - 1:
        candidate_moves.append(idx + k)
    if col > 0:
        candidate_moves.append(idx - 1)
    if col < k - 1:
        candidate_moves.append(idx + 1)

    result = []

    for m in candidate_moves:

        if board[m] == -1:
            continue

        b = list(board)
        b[idx], b[m] = b[m], b[idx]
        result.append(tuple(b))

    return result


def print_board(board: Tuple[int, ...], k: int) -> str:
    # print row by row
    lines = []
    for r in range(k):
        row = []
        start = r * k
        end = start + k
        for i in range(start, end):
            row.append(board[i])
        row_strs = []
        for x in row:
            row_strs.append(str(x))
        line = " ".join(row_strs)
        lines.append(line)
 
    result = ""
    for i in range(len(lines)):
        result += lines[i]
        if i < len(lines) - 1:
            result += "\n"
    return result
