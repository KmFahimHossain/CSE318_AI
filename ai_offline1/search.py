import heapq
import itertools
import time
from board import goal_state, neighbors

def solve(start, k, h_func, weight=1.0, time_limit=None):
    goal = goal_state(start, k)
    counter = itertools.count()  # tiebreaker so heapq never compares boards directly
    g_score = {}
    g_score[start] = 0
    came_from = {}
    came_from[start] = None
    h0 = h_func(start, k)
    open_list = []
    heapq.heappush(open_list, (weight * h0, next(counter), 0, start))
    nodes_expanded = 0
    deadline = None
    if time_limit is not None:
        deadline = time.perf_counter() + time_limit

    while len(open_list) > 0:
        if deadline is not None and time.perf_counter() > deadline:
            return None, -1, nodes_expanded

        f, _, g, board = heapq.heappop(open_list)

        # stale entry check, since heapq has no decrease-key
        best_g = g_score.get(board, float('inf'))
        if g > best_g:
            continue

        nodes_expanded += 1

        if board == goal:
            path = []
            cur = board
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            path.reverse()
            return path, g, nodes_expanded

        for nb in neighbors(board, k):
            tentative_g = g + 1
            old_g = g_score.get(nb, float('inf'))
            if tentative_g < old_g:
                g_score[nb] = tentative_g
                came_from[nb] = board
                h = h_func(nb, k)
                f = tentative_g + weight * h
                heapq.heappush(open_list, (f, next(counter), tentative_g, nb))

    return None, -1, nodes_expanded
