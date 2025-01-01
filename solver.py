from puzzle import *
import heapq as hq
from typing import Iterable, Tuple, Union

def solve(puzzle: Puzzle) -> Solution:
    return solve_from(puzzle.new_game())

def solve_from(state: GameState) -> Solution:
    if not is_valid(state):
        raise ValueError("Start state was not valid")
    return shortest_path(state)

def neighbors(state: GameState) -> Iterable[Tuple[Move, GameState]]:
    for piece in state.puzzle.pieces:
        pos = state.positions[piece.id]
        def with_move(dr, dc):
            n = state.copy()
            n.positions[piece.id] = (pos[0] + dr, pos[1] + dc)
            return n
        if pos[0] > 0:
            yield (Move(piece.id, "Up"), with_move(-1, 0))
        if pos[0] < state.puzzle.board.get_rows() - 1:
            yield (Move(piece.id, "Down"), with_move(1, 0))
        if pos[1] > 0:
            yield (Move(piece.id, "Left"), with_move(0, -1))
        if pos[1] < state.puzzle.board.get_cols() - 1:
            yield (Move(piece.id, "Right"), with_move(0, 1))

def shortest_path(start: GameState) -> Solution:
    queue = [(0, start)]
    visited = {start: 0}
    path = {start: None}
    while queue:
        _, v = hq.heappop(queue)
        if is_end(v):
            return path_to_moves(path, v)
        for (m, n) in neighbors(v):
            if not is_valid(n):
                continue
            if n not in visited or visited[n] > visited[v] + 1:
                path[n] = (v, m)
                visited[n] = visited[v] + 1
                hq.heappush(queue, (visited[v] + 1 + score(n), n))
    return []

def is_valid(state: GameState) -> bool:
    buffer = [r.copy() for r in state.puzzle.board.mask]
    for p in state.puzzle.pieces:
        pos = state.positions[p.id]
        for r, row in enumerate(p.mask):
            for c, x in enumerate(row):
                if x:
                    if buffer[pos[0] + r][pos[1] + c]:
                        return False
                    buffer[pos[0] + r][pos[1] + c] = True
    return True

def score(state: GameState) -> int:
    s = 0
    for p in state.puzzle.pieces:
        if p.goal is not None:
            pos = state.positions[p.id]
            s += abs(pos[0] - p.goal[0]) + abs(pos[1] - p.goal[1])
    return s

def is_end(state: GameState) -> bool:
    for p in state.puzzle.pieces:
        if p.goal is not None and state.positions[p.id] != p.goal:
            return False
    return True

def path_to_moves(path: Dict[GameState, Union[None, Tuple[GameState, Move]]], current: GameState) -> Solution:
    moves = []
    while (node := path.get(current)) is not None:
        current, move = node
        moves.append(move)
    moves.reverse()
    return moves
