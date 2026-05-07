from mazegen.Maze import Maze


def maze_to_hex(maze: Maze) -> list[list[str]]:
    """
    For each logical cell,  checks which surrounding walls are closed
    Sums those bit values:
    N=1, E=2, S=4, W=8
    Each sum value is then converted into hex (per cell).
    """
    hex_values: list[list[str]] = []

    grid = maze.grid
    height = maze.height
    width = maze.width

    for y in range(0, height):
        line: list[str] = []
        for x in range(0, width):
            cur_y, cur_x = (y * 2 + 1), (x * 2 + 1)  # Expanded grid
            value = 0
            if grid[cur_y - 1][cur_x] == 1:
                value += 1   # N
            if grid[cur_y][cur_x + 1] == 1:
                value += 2   # E
            if grid[cur_y + 1][cur_x] == 1:
                value += 4   # S
            if grid[cur_y][cur_x - 1] == 1:
                value += 8   # W
            line.append(hex(value)[2:].upper())
        hex_values.append(line)
    return hex_values
