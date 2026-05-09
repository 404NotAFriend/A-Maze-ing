from mlx import Mlx
from render.Assets import Assets
from mazegen.Maze import Maze


def draw_maze(
    maze: Maze,
    mlx: Mlx,
    mlx_ptr,
    win_ptr,
    tile_size: int,
    assets: Assets,
    grid: list[list[int]],
    path: list[tuple[int, int]] | None = None
) -> None:
    """
    Draw only the maze
    """

    # ---------------------------------
    # ENTRY / EXIT
    # ---------------------------------

    entry_x, entry_y = maze.entry
    exit_x, exit_y = maze.exit

    entry_x = entry_x * 2 + 1
    entry_y = entry_y * 2 + 1

    exit_x = exit_x * 2 + 1
    exit_y = exit_y * 2 + 1

    door_entry_x, door_entry_y = entry_x, entry_y
    door_exit_x, door_exit_y = exit_x, exit_y

    # ENTRY DOOR
    if entry_x == 1:
        door_entry_x -= 1
    elif entry_x == maze.grid_width - 2:
        door_entry_x += 1
    elif entry_y == 1:
        door_entry_y -= 1
    else:
        door_entry_y += 1

    # EXIT DOOR
    if exit_x == 1:
        door_exit_x -= 1
    elif exit_x == maze.grid_width - 2:
        door_exit_x += 1
    elif exit_y == 1:
        door_exit_y -= 1
    else:
        door_exit_y += 1

    # ---------------------------------
    # DRAW PATH
    # ---------------------------------

    solved_grid = [row[:] for row in grid]

    if path is not None:

        visual_path = [
            (door_entry_y, door_entry_x),
            *path
        ]

        for (y, x) in visual_path[:-1]:
            solved_grid[y][x] = 4
        current_y, current_x = visual_path[-1]

        if (current_y, current_x) == (exit_y, exit_x):
            solved_grid[current_y][current_x] = 4
            current_y, current_x = door_exit_y, door_exit_x

        solved_grid[current_y][current_x] = 3

    for grid_y, row in enumerate(solved_grid):
        for grid_x, cell in enumerate(row):
            # Convert grid -> pixels
            screen_x = grid_x * tile_size
            screen_y = grid_y * tile_size

            # ENTRY
            if (grid_x,grid_y) == (door_entry_x, door_entry_y):
                tile = assets.duck

            # EXIT
            elif (grid_x, grid_y) == (door_exit_x, door_exit_y):
                tile = assets.duck
            elif cell == 3:
                tile = assets.duck
            elif cell == 0:
                tile = assets.floor
            elif cell == 1:
                tile = assets.wall
            elif cell == 2:
                tile = assets.wall_42
            else:
                tile = assets.trail

            # DRAW TILE
            mlx.mlx_put_image_to_window(
                mlx_ptr,
                win_ptr,
                tile,
                screen_x,
                screen_y
            )

