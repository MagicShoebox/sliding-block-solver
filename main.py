from puzzle import *
from solver import solve_from
import json
import sys

def main(filename: str):
    with open(filename, 'r') as file:
        data = json.load(file)
    state = JsonPuzzle \
        .deserialize(data) \
        .get_puzzle() \
        .new_game()
    print(state)
    print()
    solution = solve_from(state)
    for move in solution:
        print(move)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    main(filename)
