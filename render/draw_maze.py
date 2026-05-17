from mlx import Mlx
from render.Assets import Assets
from render.constants import (maze_offset_x, maze_offset_y)
from mazegen.Maze import Maze
from typing import Any
import time


def logical_to_grid(logical_x: int, logical_y: int) -> tuple[int, int]:
    """
    Convert logical maze coordinates to grid coordinates.
    Logical coordinates (0,0) become grid coordinates (1,1).
    """
    return logical_x * 2 + 1, logical_y * 2 + 1


def grid_to_logical(grid_x: int, grid_y: int) -> tuple[int, int]:
    """
    Convert grid coordinates to logical maze coordinates.
    Grid coordinates (1,1) become logical coordinates (0,0).
    """
    return (grid_x - 1) // 2, (grid_y - 1) // 2


def calculate_door_position(
    logical_x: int,
    logical_y: int,
    maze: Maze
) -> tuple[int, int]:
    """
    Calculate the visual door position from logical coordinates.
    The door is placed 1 cell away from the logical position
    towards the maze edge.
    """
    grid_x, grid_y = logical_to_grid(logical_x, logical_y)
    door_x, door_y = grid_x, grid_y

    if grid_x == 1:
        door_x -= 1
    elif grid_x == maze.grid_width - 2:
        door_x += 1
    elif grid_y == 1:
        door_y -= 1
    else:
        door_y += 1

    return door_x, door_y


def draw_maze(
    maze: Maze,
    mlx: Mlx,
    mlx_ptr: Any,
    win_ptr: Any,
    tile_size: int,
    assets: Assets,
    grid: list[list[int]],
    path: list[tuple[int, int]] | None = None,
    show_duck: bool = True,
    duck_position: tuple[int, int] | None = None,
    animate_exit: bool = False
) -> None:
    """
    Draw the maze with mlx.
    Maze is centered horizontally and vertically
    within the maze area (above the banner).
    """

    # ---------------------------------
    # ENTRY / EXIT
    # ---------------------------------

    entry_x, entry_y = maze.entry
    exit_x, exit_y = maze.exit

    entry_x, entry_y = logical_to_grid(entry_x, entry_y)
    exit_x, exit_y = logical_to_grid(exit_x, exit_y)

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
            *path,
        ]

        for (y, x) in visual_path[:-1]:
            solved_grid[y][x] = 4

        current_y, current_x = visual_path[-1]

        if (current_y, current_x) == (exit_y, exit_x):
            solved_grid[current_y][current_x] = 4
            current_y, current_x = door_exit_y, door_exit_x

        if duck_position is not None:
            duck_y, duck_x = duck_position
            solved_grid[duck_y][duck_x] = 3
        elif show_duck:
            solved_grid[current_y][current_x] = 3

    # ---------------------------------
    # CENTERING
    # ---------------------------------

    # Center maze horizontally in full window width
    # Center maze vertically in maze area only (above banner)
    offset_x: int = maze_offset_x(maze.grid_width, tile_size)
    offset_y: int = maze_offset_y(maze.grid_height, tile_size)

    # ---------------------------------
    # DRAW TILES
    # ---------------------------------

    for grid_y, row in enumerate(solved_grid):
        for grid_x, cell in enumerate(row):

            screen_x: int = offset_x + (grid_x * tile_size)
            screen_y: int = offset_y + (grid_y * tile_size)

            # Draw floor first for duck positions
            if cell == 3:
                base_tile = assets.floor
            elif cell == 0:
                base_tile = assets.floor
            elif cell == 1:
                base_tile = assets.wall
            elif cell == 2:
                base_tile = assets.wall_42
            else:
                base_tile = assets.trail

            # Draw base tile
            mlx.mlx_put_image_to_window(
                mlx_ptr,
                win_ptr,
                base_tile,
                screen_x,
                screen_y
            )

            # Draw duck on top
            if cell == 3:
                mlx.mlx_put_image_to_window(
                    mlx_ptr,
                    win_ptr,
                    assets.duck,
                    screen_x,
                    screen_y
                )

            # EXIT (with animation when duck reaches it)
            if (grid_x, grid_y) == (door_exit_x, door_exit_y):
                if animate_exit:
                    animation_frame = int(time.time() * 3.33) % 2
                    exit_image = (
                        assets.exit2
                        if animation_frame == 1
                        else assets.exit
                    )
                else:
                    exit_image = assets.exit

                mlx.mlx_put_image_to_window(
                    mlx_ptr,
                    win_ptr,
                    exit_image,
                    screen_x,
                    screen_y
                )
