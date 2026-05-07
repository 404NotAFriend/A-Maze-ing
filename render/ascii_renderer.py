from mazegen.Maze import Maze


def render_ascii(grid: list[list[int]],
                 maze: Maze,
                 path: list[tuple[int, int]] | None = None) -> None:
    """
    TEMPORARY - 0 prints . / 1 prints # / X in path (bfs solver)
    """
    solved_grid = [row[:] for row in grid]

    entry_x, entry_y = maze.entry
    exit_x, exit_y = maze.exit

    entry_cell = (entry_y * 2 + 1, entry_x * 2 + 1)
    exit_cell = (exit_y * 2 + 1, exit_x * 2 + 1)

    # Calculate the real pos of the entry and exit
    if entry_x == 0:
        entry_pos = (entry_cell[0], entry_cell[1] - 1)
    elif entry_x == maze.width - 1:
        entry_pos = (entry_cell[0], entry_cell[1] + 1)
    elif entry_y == 0:
        entry_pos = (entry_cell[0] - 1, entry_cell[1])
    else:  # entry_y == height - 1
        entry_pos = (entry_cell[0] + 1, entry_cell[1])

    if exit_x == 0:
        exit_pos = (exit_cell[0], exit_cell[1] - 1)
    elif exit_x == maze.width - 1:
        exit_pos = (exit_cell[0], exit_cell[1] + 1)
    elif exit_y == 0:
        exit_pos = (exit_cell[0] - 1, exit_cell[1])
    else:  # exit_y == height - 1
        exit_pos = (exit_cell[0] + 1, exit_cell[1])

    if path is not None:
        for (y, x) in path:
            solved_grid[y][x] = 3

    for y, row in enumerate(solved_grid):
        line = ""
        for x, cell in enumerate(row):
            if (y, x) == entry_pos:
                line += "\033[92mS\033[0m"

            elif (y, x) == exit_pos:
                line += "\033[92mE\033[0m"

            elif cell == 3:
                line += "\033[94m.\033[0m"

            elif cell == 0:
                line += " "

            elif cell == 2:
                line += "\033[91m■\033[0m"

            else:
                line += "#"
        print(line)
