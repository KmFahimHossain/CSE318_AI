from typing import Tuple, List

def goal_state(k: int) -> Tuple[int, ...]:
    # 1 to n-1, then 0 (blank) at the end
    return tuple(list(range(1, k * k)) + [0])

def blank_index(board: Tuple[int, ...]) -> int:
    return board.index(0)

def is_solvable(board: Tuple[int, ...], k: int) -> bool:
    seq = []
    for t in board:
        if t != 0:  # skip if it is blank
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


def neighbors(board: Tuple[int, ...], k: int) -> List[Tuple[int, ...]]:
    idx = blank_index(board)  # blank's position in flat tuple
    row = idx // k
    col = idx % k
 
    # check which directions are in bounds
    moves = []
    if row > 0:
        moves.append(idx - k)  # up
    if row < k - 1:
        moves.append(idx + k)  # down
    if col > 0:
        moves.append(idx - 1)  # left
    if col < k - 1:
        moves.append(idx + 1)  # right
 
    # swap blank with each valid neighbor -> new board states
    result = []
    for m in moves:
        b = list(board)
        temp = b[idx]
        b[idx] = b[m]
        b[m] = temp
        new_board = tuple(b)
        result.append(new_board)
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
