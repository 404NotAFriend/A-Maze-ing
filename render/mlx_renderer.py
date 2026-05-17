from mlx import Mlx
from typing import Any
from render.Assets import Assets
from render.converter import generate_all_assets
from render.draw_maze import (draw_maze,
                              calculate_door_position,
                              logical_to_grid,
                              grid_to_logical)
from render.menu import (_prepare_menu_images, _draw_menu, _draw_banner)
from render.GameState import GameState
from render.constants import WINDOW_WIDTH, WINDOW_HEIGHT, MAZE_AREA_HEIGHT
import os
import time

# ---------------------------------
# GAME EVENTS
# ---------------------------------

KEY_ESC: int = 65307
KEY_1: int = 49
KEY_2: int = 50
KEY_3: int = 51
KEY_4: int = 52
KEY_5: int = 53
KEY_6: int = 54
KEY_UP: int = 65362
KEY_DOWN: int = 65364
KEY_LEFT: int = 65361
KEY_RIGHT: int = 65363


def close(param: Any) -> None:
    """Close the window"""
    os._exit(0)


def key_hook(key: int, game: GameState, frame: list[int],
             param: Any, mlx: Any = None, mlx_ptr: Any = None,
             win_ptr: Any = None) -> None:
    """Menu and banner game options"""

    if game.mode == "MENU":
        if key == KEY_1:
            game.theme = "normal"
            game.mode = "GAME"
            game.clear_screen = True
        elif key == KEY_2:
            game.theme = "gothic"
            game.mode = "GAME"
            game.clear_screen = True

    elif game.mode == "GAME":
        # STATIC ENTRY ON THE GAME
        if key == KEY_1:

            # Reset game state
            game.mode = "GAME"
            game.clear_screen = True
            game.reload_assets = True
            game.game_won = False
            game.playing = False
            game.show_path = False
            game.animate_bfs = False
            game.show_duck = True

            # Reset animation/frame state
            frame[0] = 0
            game.player_path = []
            game.path_animation_complete = False
            game.bfs_animation_complete = False

            # Generate new maze
            if game.generator is None:
                return

            game.maze = game.generator.generate_maze()
            game.path, game.explored = game.generator.solve("bfs")

            # Export maze
            if game.output_file is not None:
                game.generator.export(game.output_file)

            # Reset player position
            if game.maze is None:
                return

            game.player_x, game.player_y = game.maze.entry

            (
                game.player_grid_x,
                game.player_grid_y
            ) = logical_to_grid(
                game.player_x,
                game.player_y
            )

            # Clear and sync window
            if mlx and mlx_ptr and win_ptr:
                mlx.mlx_clear_window(mlx_ptr, win_ptr)
                mlx.mlx_do_sync(mlx_ptr)

        # 2 - SHOW PATH ANIMATION
        if key == KEY_2:
            game.playing = False
            game.game_won = False
            game.show_path = True
            game.animate_bfs = False
            game.show_duck = True
            game.player_path = []  # Clear any player trail
            # Reset animation flags
            game.path_animation_complete = False
            game.bfs_animation_complete = False
            frame[0] = 0  # Restart animation

        # 3 - SHOW PATH FINDER
        if key == KEY_3:
            # Reset for BFS animation mode
            game.playing = False
            game.game_won = False
            game.show_path = False
            game.animate_bfs = True
            game.show_duck = False  # No duck in BFS mode
            game.player_path = []  # Clear any player trail
            # Bruno -> Reset animation flags
            game.path_animation_complete = False
            game.bfs_animation_complete = False
            frame[0] = 0  # Restart animation

        # 4 - PLAYER MODE
        if key == KEY_4:
            if mlx and mlx_ptr and win_ptr:
                mlx.mlx_clear_window(mlx_ptr, win_ptr)
                mlx.mlx_do_sync(mlx_ptr)

            game.playing = True
            game.game_won = False
            game.show_path = False
            game.animate_bfs = False
            game.show_duck = True
            frame[0] = 0
            game.path_animation_complete = False
            game.bfs_animation_complete = False
            if game.maze is None:
                return
            entry_x, entry_y = game.maze.entry
            (door_entry_x, door_entry_y) = calculate_door_position(entry_x,
                                                                   entry_y,
                                                                   game.maze)

            game.player_grid_x = door_entry_x
            game.player_grid_y = door_entry_y
            game.player_x, game.player_y = grid_to_logical(door_entry_x,
                                                           door_entry_y)
            game.player_path = [(door_entry_y, door_entry_x)]

        # 5 - CHANGE THEME
        if key == KEY_5:
            game.clear_screen = True
            game.reload_assets = True
            game.show_path = False
            game.animate_bfs = False
            game.show_duck = True
            if game.theme == "normal":
                game.theme = "gothic"
            else:
                game.theme = "normal"
            game.show_path = False

        # Handle player movement in player mode (only for arrow keys)
        if game.playing and key in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
            handle_player_movement(key, game)

    # ESC | 6 - QUIT GAME
    if key == KEY_ESC or key == KEY_6:
        os._exit(0)


def handle_player_movement(key: int, game: GameState) -> None:
    """Handle arrow key movement for player mode - smooth grid movement"""
    if not game.playing or game.maze is None or game.game_won:
        return

    # Calculate new grid position (move by 1 grid step)
    new_grid_x, new_grid_y = game.player_grid_x, game.player_grid_y

    if key == KEY_UP:
        new_grid_y -= 1
    elif key == KEY_DOWN:
        new_grid_y += 1
    elif key == KEY_LEFT:
        new_grid_x -= 1
    elif key == KEY_RIGHT:
        new_grid_x += 1

    # Check bounds
    if not (0 <= new_grid_y < game.maze.grid_height and
            0 <= new_grid_x < game.maze.grid_width):
        return

    # Check if position is blocked
    if (
        game.maze.grid[new_grid_y][new_grid_x] == 1
        or game.maze.grid[new_grid_y][new_grid_x] == 2
    ):
        return

    # Handle trail/backtracking
    # If going backwards (to previous position), remove trail
    if (
        len(game.player_path) > 1
        and
        (new_grid_y, new_grid_x) == game.player_path[-2]
    ):
        game.player_path.pop()
    else:
        # Add new position to trail
        game.player_path.append((new_grid_y, new_grid_x))

    # Update grid position
    game.player_grid_x = new_grid_x
    game.player_grid_y = new_grid_y

    # Update logical position using utility function
    game.player_x, game.player_y = grid_to_logical(new_grid_x, new_grid_y)

    # Check if exit reached using helper function
    exit_x, exit_y = game.maze.exit
    door_exit_x, door_exit_y = calculate_door_position(exit_x,
                                                       exit_y,
                                                       game.maze)

    if (game.player_grid_x, game.player_grid_y) == (door_exit_x, door_exit_y):
        print("🎉 Congratulations! You reached the exit!")
        print("🎉 Game Won! Press 1 to play again or ESC to quit.")
        game.game_won = True
        game.playing = False  # Stop player movement


# ---------------------------------
# TILE SIZE
# ---------------------------------

def calculate_tile_size(game: GameState) -> int:
    """
    Dynamically calculate tile size
    so the maze fits the window above the banner
    """
    if game.maze is None:
        return 32
    tile_width: int = WINDOW_WIDTH // game.maze.grid_width
    tile_height: int = MAZE_AREA_HEIGHT // game.maze.grid_height
    return min(tile_width, tile_height)


# ---------------------------------
# GAME WINDOW
# ---------------------------------

def mlx_window(game: GameState) -> None:
    """Opens the game window"""
    # TILE AND WINDOW SIZE
    tile_size = calculate_tile_size(game)

    # GENERATE ASSETS
    generate_all_assets(tile_size)

    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    win_ptr = mlx.mlx_new_window(
        mlx_ptr,
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        "A-MAZE-ING"
    )

    # ASSETS
    assets: list[Assets | None] = [None]
    menu_imgs = _prepare_menu_images(mlx, mlx_ptr)

    # DRAW
    frame = [0]
    last_time = [time.time()]

    mlx.mlx_key_hook(
        win_ptr,
        lambda key, param: key_hook(
            key,
            game,
            frame,
            param,
            mlx,
            mlx_ptr,
            win_ptr
            ),
        None
    )

    def on_loop(param: Any) -> None:
        """Loop to handle options on window"""

        # -------------------------
        # CLEAR WINDOW
        # -------------------------

        # CLEAR OLD MENU ONLY ONCE
        if game.clear_screen:
            mlx.mlx_clear_window(mlx_ptr, win_ptr)
            game.clear_screen = False

        if game.mode == "MENU":
            mlx.mlx_clear_window(
                mlx_ptr,
                win_ptr
            )

        # -------------------------
        # MENU
        # -------------------------

        if game.mode == "MENU":

            _draw_menu(
                mlx,
                mlx_ptr,
                win_ptr,
                menu_imgs
            )

        # -------------------------
        # GAME
        # -------------------------

        elif game.mode == "GAME":

            # LOAD ASSETS OR RELOAD (change theme onption)
            if game.reload_assets:
                assets[0] = None
                game.reload_assets = False
            if game.theme is None:
                return
            if assets[0] is None:

                assets[0] = Assets(
                    mlx,
                    mlx_ptr,
                    tile_size,
                    game.theme
                )

            if game.path is None:
                return
            if game.maze is None:
                return
            if game.explored is None:
                return
            if assets[0] is None:
                return

            # SHOW PATH ANIMATION - Option 2
            if game.show_path:
                now = time.time()

                # Check if path animation has completed (duck reached exit)
                if frame[0] >= len(game.path) and len(game.path) > 0:
                    game.path_animation_complete = True

                duck_at_exit = game.path_animation_complete

                # Continue animation for exit portal,
                # or run normal path animation
                if (
                    frame[0] <= len(game.path) or duck_at_exit
                ) and now - last_time[0] >= 0.02:

                    draw_maze(
                        game.maze,
                        mlx,
                        mlx_ptr,
                        win_ptr,
                        tile_size,
                        assets[0],
                        game.maze.grid,
                        game.path[:frame[0]]
                        if frame[0] > 0
                        else None,
                        show_duck=True,
                        duck_position=None,
                        animate_exit=duck_at_exit
                    )

                    # Draw banner UI at bottom
                    _draw_banner(mlx, mlx_ptr, win_ptr, menu_imgs)

                    frame[0] += 1
                    last_time[0] = now

            # SHOW PATH FINDER BFS ANIMATION - Option 3
            elif game.animate_bfs:
                now = time.time()

                # Check if BFS animation has completed (found exit)
                if frame[0] >= len(game.explored) and len(game.explored) > 0:
                    game.bfs_animation_complete = True

                bfs_at_exit = game.bfs_animation_complete

                # Continue animation for exit portal,
                # or run normal BFS animation
                if (
                    frame[0] <= len(game.explored) or bfs_at_exit
                ) and now - last_time[0] >= 0.05:

                    draw_maze(
                        game.maze,
                        mlx,
                        mlx_ptr,
                        win_ptr,
                        tile_size,
                        assets[0],
                        game.maze.grid,
                        game.explored[:frame[0]]
                        if frame[0] > 0
                        else None,
                        show_duck=False,
                        duck_position=None,
                        animate_exit=bfs_at_exit
                    )

                    # Bruno -> Draw banner UI at bottom
                    _draw_banner(mlx, mlx_ptr, win_ptr, menu_imgs)

                    frame[0] += 1
                    last_time[0] = now

            # STATIC MAZE
            else:
                # Determine duck position for player mode
                duck_position = None
                if game.playing:
                    duck_position = (game.player_grid_y, game.player_grid_x)

                # Check if player has won for exit animation
                player_at_exit = game.game_won

                draw_maze(
                    game.maze,
                    mlx,
                    mlx_ptr,
                    win_ptr,
                    tile_size,
                    assets[0],
                    game.maze.grid,
                    game.player_path,
                    show_duck=True,
                    duck_position=duck_position,
                    animate_exit=player_at_exit
                )

                # Bruno -> Draw banner UI at bottom
                _draw_banner(mlx, mlx_ptr, win_ptr, menu_imgs)

                # Conservative sync after static/player rendering
                mlx.mlx_do_sync(mlx_ptr)

    # WINDOW EVENTS
    mlx.mlx_hook(
        win_ptr,
        33,
        0,
        close,
        None
    )

    mlx.mlx_loop_hook(
        mlx_ptr,
        on_loop,
        None
    )
    mlx.mlx_loop(mlx_ptr)
