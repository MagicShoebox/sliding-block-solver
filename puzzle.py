from typing import List, Dict, Tuple

class Piece:
    def __init__(self, id: str, symbol: str, start: Tuple[int, int], mask: List[List[bool]], goal: Tuple[int, int] = None):
        self.id = id
        self.symbol = symbol
        self.start = start
        self.goal = goal
        self.mask = mask

class Board:
    def __init__(self, symbol: str, mask: List[List[bool]]):
        self.symbol = symbol
        self.mask = mask

    def get_rows(self) -> int:
        return len(self.mask)
    
    def get_cols(self) -> int:
        return len(self.mask[0])

class Puzzle:
    def __init__(self, board: Board, pieces: List[Piece]):
        self.board = board
        self.pieces = pieces
    
    def new_game(self):
        return GameState(puzzle=self, positions={p.id: p.start for p in self.pieces})
    
    def deserialize(data: any) -> 'Puzzle':
        board_mask = [[bool(x) for x in row] for row in data["board"]["mask"]]
        board = Board(symbol=data["board"]["symbol"], mask=board_mask)
        pieces = []
        for piece_data in data["pieces"]:
            piece_mask = [[bool(x) for x in row] for row in piece_data["mask"]]
            piece = Piece(
                id=piece_data["id"],
                symbol=piece_data["symbol"],
                start=tuple(piece_data["start"]),
                mask=piece_mask,
                goal=tuple(g) if (g := piece_data.get("goal")) is not None else None
            )
            pieces.append(piece)
        
        return Puzzle(board=board, pieces=pieces)

class JsonPuzzle:
    def __init__(self, version: str, type: str, data: str):
        self.version = version
        self.type = type
        self.data = data
    
    def deserialize(data: any) -> 'JsonPuzzle':
        return JsonPuzzle(version=data["version"], type=data["type"], data=data["data"])

    def get_puzzle(self) -> Puzzle:
        return Puzzle.deserialize(self.data)

class GameState:
    def __init__(self, puzzle: Puzzle, positions: Dict[str, Tuple[int, int]]):
        self.puzzle = puzzle
        self.positions = positions

    def __hash__(self):
        return hash(tuple((id, r, c) for id, (r, c) in self.positions.items()))
    
    def __eq__(self, value):
        return isinstance(value, GameState) and self.positions == value.positions
    
    def __str__(self):
        buffer = [['.' for _ in row] for row in self.puzzle.board.mask]
        for r, row in enumerate(self.puzzle.board.mask):
            for c, x in enumerate(row):
                if x:
                    buffer[r][c] = self.puzzle.board.symbol
        for piece in self.puzzle.pieces:
            pos = self.positions[piece.id]
            for r, row in enumerate(piece.mask):
                for c, x in enumerate(row):
                    if x:
                        buffer[pos[0] + r][pos[1] + c] = piece.symbol
        return '\n'.join((''.join(line) for line in buffer))
    
    def __lt__(self, value):
        return hash(self) < hash(value)

    def copy(self) -> 'GameState':
        return GameState(puzzle=self.puzzle, positions={id: pos for (id, pos) in self.positions.items()})

class Move:
    def __init__(self, id: str, dir: str):
        self.id = id
        self.dir = dir
    
    def __str__(self):
        return f"{self.id} {self.dir}"
    
Solution = List[Move]
