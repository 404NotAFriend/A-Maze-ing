from mlx import Mlx
from render.Assets import Assets
from mazegen.Maze import Maze
from render.converter import generate_all_assets
from render.draw_maze import draw_maze
import os
import time


# ---------------------------------
# WINDOW
# ---------------------------------

MAX_WINDOW_WIDTH = 1400
MAX_WINDOW_HEIGHT = 1800

# ---------------------------------
# CLOSE WINDOW
# ---------------------------------

def close(param) -> None:
    """Close the window"""

    os._exit(0)


def key_hook(key, param) -> None:
    """Close with ESC"""

    ESC_KEY = 65307

    if key == ESC_KEY:
        os._exit(0)


# ---------------------------------
# TILE SIZE
# ---------------------------------

def calculate_tile_size(
    maze: Maze) -> int:
    """
    Dynamically calculate tile size
    so the maze fits the window
    """

    maze_height = maze.grid_height

    maze_width = maze.grid_width

    tile_width = (
        MAX_WINDOW_WIDTH // maze_width
    )

    tile_height = (
        MAX_WINDOW_HEIGHT // maze_height
    )

    return min(
        tile_width,
        tile_height
    )

# ---------------------------------
# MAIN WINDOW
# ---------------------------------

def mlx_window(maze: Maze,
               path: list[tuple[int, int]],
               theme: str) -> None:

    # -------------------------
    # TILE AND WINDOW SIZE
    # -------------------------

    tile_size = calculate_tile_size(
        maze
    )

    window_width = (
        maze.grid_width * tile_size
    )

    window_height = (
        maze.grid_height * tile_size
    )

    # -------------------------
    # GENERATE ASSETS
    # -------------------------

    generate_all_assets(
        tile_size
    )

    # -------------------------
    # MLX
    # -------------------------

    mlx = Mlx()

    mlx_ptr = mlx.mlx_init()

    win_ptr = mlx.mlx_new_window(
        mlx_ptr,
        window_width,
        window_height,
        "A-MAZE-ING"
    )

    mlx.mlx_hook(win_ptr, 33, 0, close, None)
    mlx.mlx_key_hook(win_ptr, key_hook, None)

    # -------------------------
    # ASSETS
    # -------------------------

    assets = Assets(
        mlx,
        mlx_ptr,
        tile_size,
        theme
    )

    # -------------------------
    # DRAW
    # -------------------------

    for i in range(1, len(path) + 1):
        draw_maze(
            maze,
            mlx,
            mlx_ptr,
            win_ptr,
            tile_size,
            assets,
            maze.grid,
            path[:i]
        )

        time.sleep(0.1)
    mlx.mlx_loop(mlx_ptr)
