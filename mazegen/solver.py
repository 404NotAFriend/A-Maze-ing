from collections import deque
from mazegen.Maze import Maze


def bfs_solve_maze(maze: Maze) -> tuple[list[tuple[int, int]],
                                        list[tuple[int, int]]]:
    """
    Finds the shortest path to solve the maze
    With Breadth First Search (BFS)
    """
    grid = maze.grid
    height = maze.grid_height
    width = maze.grid_width
    x1, y1 = maze.entry
    x2, y2 = maze.exit

    # Convert entry / exit to the expanded grid
    (entry_x, entry_y) = (x1 * 2 + 1), (y1 * 2 + 1)
    (exit_x, exit_y) = (x2 * 2 + 1), (y2 * 2 + 1)

    queue: deque[tuple[int, int]] = deque()
    visited: set[tuple[int, int]] = set()
    explored: list[tuple[int, int]] = []  # To show the path finder animation
    parent: dict[tuple[int, int], tuple[int, int]] = {}  # prev and curr pos

    start = (entry_y, entry_x)
    end = (exit_y, exit_x)

    # start -> entry point
    queue.append(start)
    visited.add(start)
    explored.append(start)

    directions = [
        (0, -1),  # UP
        (0, 1),   # DOWN
        (-1, 0),  # LEFT
        (1, 0)    # RIGHT
    ]

    # Find all open elements from the starting point and so on
    # Until the exit is found
    while queue:
        y, x = queue.popleft()

        if (y, x) == end:
            break

        for dy, dx in directions:
            new_y = y + dy
            new_x = x + dx

            # Check if the new y, x is inside of the maze bonds
            if not (0 <= new_y < height and 0 <= new_x < width):
                continue

            # Check if its a wall or logo
            if grid[new_y][new_x] == 1 or grid[new_y][new_x] == 2:
                continue

            # Check if it was already visited
            if (new_y, new_x) in visited:
                continue

            visited.add((new_y, new_x))
            explored.append((new_y, new_x))
            parent[(new_y, new_x)] = (y, x)
            queue.append((new_y, new_x))

    try:
        # Reconstruct the path (option 2 on the banner menu)
        path: list[tuple[int, int]] = []
        current = end

        while current != start:
            path.append(current)
            current = parent[current]

        path.append(start)
        # Get the result from the start to the exit point
        path.reverse()
    except KeyError:
        return [], explored
    return path, explored
