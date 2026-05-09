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

MAX_WINDOW_WIDTH = 1600
MAX_WINDOW_HEIGHT = 900

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
    
    frame = [0]
    last_time = [time.time()]

    def on_loop(param) -> None:
        now = time.time()
        if frame[0] <= len(path) and now - last_time[0] >= 0.05:
            draw_maze(
                maze,
                mlx,
                mlx_ptr,
                win_ptr,
                tile_size,
                assets,
                maze.grid,
                path[:frame[0]] if frame[0] > 0 else None,
            )
            frame[0] += 1
            last_time[0] = now

    mlx.mlx_loop_hook(mlx_ptr, on_loop, None)  
    mlx.mlx_loop(mlx_ptr)
