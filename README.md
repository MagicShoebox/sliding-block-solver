## Sliding Block Solver
A prototype tool I whipped up to solve sliding block puzzles, like [this one](https://layton.fandom.com/wiki/Puzzle:The_Diabolical_Box) from the second Professor Layton game. It works by doing A* traversal on a graph of game states. See [layton_db_153.json](layton_db_153.json) for an example of the input format.

I used Microsoft Copilot to help generate some of the `main.py` and JSON deserialization boilerplate. I haven't bothered to clean it up.

I'm sure the tool could be optimized more, but it worked to solve the intended puzzle.
