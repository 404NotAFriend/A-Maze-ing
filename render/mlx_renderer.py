from mlx import Mlx
from render.Assets import Assets
from render.resize import generate_all_assets
import os


# ---------------------------------
# WINDOW
# ---------------------------------

WINDOW_WIDTH = 1650
WINDOW_HEIGHT = 1350

TILE_SIZE = 64


# ---------------------------------
# SIMPLE TEST MAZE
# ---------------------------------

maze = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]


# ---------------------------------
# ENTRY / EXIT
# ---------------------------------

ENTRY = (1, 0)

EXIT = (5, 6)


# ---------------------------------
# CLOSE WINDOW
# ---------------------------------

def close(param) -> None:
    """Close the window"""

    os._exit(0)


# ---------------------------------
# ESC KEY
# ---------------------------------

def key_hook(key, param) -> None:
    """Close with ESC"""

    ESC_KEY = 65307

    if key == ESC_KEY:
        os._exit(0)


# ---------------------------------
# DRAW MAZE
# ---------------------------------

def draw_maze(
    mlx: Mlx,
    mlx_ptr,
    win_ptr,
    assets: Assets
) -> None:
    """
    Draw only the maze
    """

    for grid_y, row in enumerate(maze):

        for grid_x, cell in enumerate(row):

            # Convert grid -> pixels
            screen_x = (
                grid_x * TILE_SIZE
            )

            screen_y = (
                grid_y * TILE_SIZE
            )

            # ---------------------
            # ENTRY
            # ---------------------

            if (
                grid_x,
                grid_y
            ) == ENTRY:

                tile = assets.floor_normal

            # ---------------------
            # EXIT
            # ---------------------

            elif (
                grid_x,
                grid_y
            ) == EXIT:

                tile = assets.floor_normal

            # ---------------------
            # WALL
            # ---------------------

            elif cell == 1:

                tile = assets.wall

            # ---------------------
            # FLOOR
            # ---------------------

            else:

                tile = assets.floor_normal

            # Draw tile
            mlx.mlx_put_image_to_window(
                mlx_ptr,
                win_ptr,
                tile,
                screen_x,
                screen_y
            )


# ---------------------------------
# MAIN WINDOW
# ---------------------------------

def mlx_window() -> None:

    mlx = Mlx()

    mlx_ptr = mlx.mlx_init()

    win_ptr = mlx.mlx_new_window(
        mlx_ptr,
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        "A-MAZE-ING"
    )

    # -------------------------
    # HOOKS
    # -------------------------

    mlx.mlx_hook(
        win_ptr,
        33,
        0,
        close,
        None
    )

    mlx.mlx_key_hook(
        win_ptr,
        key_hook,
        None
    )

    # -------------------------
    # GENERATE ASSETS
    # -------------------------

    generate_all_assets(TILE_SIZE)

    # -------------------------
    # ASSETS
    # -------------------------

    assets = Assets(
        mlx,
        mlx_ptr,
        TILE_SIZE
    )

    # -------------------------
    # DRAW MAZE
    # -------------------------

    draw_maze(
        mlx,
        mlx_ptr,
        win_ptr,
        assets
    )

    # -------------------------
    # LOOP
    # -------------------------

    mlx.mlx_loop(mlx_ptr)