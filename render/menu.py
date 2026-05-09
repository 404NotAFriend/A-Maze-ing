"""Main menu and app state machine for A-Maze-ing."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from PIL import Image  # type: ignore
from mlx import Mlx  # type: ignore

from mazegen.MazeGenerator import MazeGenerator
from mazegen.Maze import Maze
from render.Assets import Assets
from render.converter import generate_all_assets
from render.draw_maze import draw_maze


# ── Window ────────────────────────────────────────────────
WINDOW_WIDTH: int = 1600
WINDOW_HEIGHT: int = 900

# ── Key codes ─────────────────────────────────────────────
KEY_ESC: int = 65307
KEY_1: int = 49
KEY_2: int = 50

# ── Theme names ───────────────────────────────────────────
THEME_LIGHT: str = "normal"
THEME_DARK: str = "gothic"


@dataclass
class MenuImages:
    """Pre-loaded MLX image pointers for the menu scene."""

    bg: Any = None


@dataclass
class AppState:
    """Mutable state shared across all MLX event hooks."""

    scene: str = "menu"
    maze: Maze | None = None
    path: list[tuple[int, int]] = field(default_factory=list)
    theme: str = "normal"
    show_path: bool = True
    needs_redraw: bool = True
    tile_size: int = 0
    assets: Assets | None = None
    menu_imgs: MenuImages | None = None


# ── Asset helpers ─────────────────────────────────────────

def _prepare_menu_images(
    mlx: Mlx, mlx_ptr: Any
) -> MenuImages:
    """
    Generate and load all images needed for the menu scene.

    All assets use the XPM format (via magick) with
    dimensions in the filename so any size change triggers
    a fresh generation rather than reusing stale cache.

    Args:
        mlx: Mlx instance.
        mlx_ptr: MLX connection pointer.

    Returns:
        MenuImages with every pointer filled.
    """
    os.makedirs("assets/generated", exist_ok=True)
    imgs = MenuImages()

    bg_xpm = (
        f"assets/generated/"
        f"menu_bgnew_{WINDOW_WIDTH}x{WINDOW_HEIGHT}.xpm"
    )
    if not os.path.exists(bg_xpm):
        bg_png = bg_xpm.replace(".xpm", ".png")
        if not os.path.exists(bg_png):
            src = Image.open(
                "assets/imgs/menu_backgroundnew.png"
            )
            src = src.resize(
                (WINDOW_WIDTH, WINDOW_HEIGHT), Image.LANCZOS
            )
            src.save(bg_png)
        os.system(f"magick {bg_png} {bg_xpm}")
    imgs.bg, _, _ = mlx.mlx_xpm_file_to_image(
        mlx_ptr, bg_xpm
    )

    return imgs


# ── Menu rendering ────────────────────────────────────────

def _draw_menu(
    mlx: Mlx,
    mlx_ptr: Any,
    win_ptr: Any,
    state: AppState,
) -> None:
    """
    Render the difficulty-selection menu.

    Args:
        mlx: Mlx instance.
        mlx_ptr: MLX connection pointer.
        win_ptr: Window pointer.
        state: Current application state.
    """
    imgs = state.menu_imgs
    if imgs is None:
        return

    mlx.mlx_put_image_to_window(
        mlx_ptr, win_ptr, imgs.bg, 0, 0
    )


# ── Maze setup helpers ────────────────────────────────────

def _build_maze(
    config: dict[str, Any],
) -> tuple[Maze, list[tuple[int, int]]]:
    """
    Generate a maze and compute its shortest path.

    Args:
        config: Preset dict with all maze parameters.

    Returns:
        Tuple of (Maze instance, BFS path).
    """
    gen = MazeGenerator(
        config["WIDTH"],
        config["HEIGHT"],
        config["ENTRY"],
        config["EXIT"],
        config["PERFECT"],
        config.get("SEED"),
    )
    maze = gen.generate_maze()
    path = gen.solve("bfs")
    gen.export(config["OUTPUT_FILE"])
    return maze, path


def _tile_size_for_window(maze: Maze) -> int:
    """
    Largest tile size that fits the maze inside the window.

    Args:
        maze: Generated maze instance.

    Returns:
        Tile size in pixels (minimum 1).
    """
    return max(
        1,
        min(
            WINDOW_WIDTH // maze.grid_width,
            WINDOW_HEIGHT // maze.grid_height,
        ),
    )


def _transition_to_maze(
    mlx: Mlx,
    mlx_ptr: Any,
    config: dict[str, Any],
    theme: str,
    state: AppState,
) -> None:
    """
    Generate the maze from config, load assets, switch scene.

    Args:
        mlx: Mlx instance.
        mlx_ptr: MLX connection pointer.
        config: Parsed config dict from config.txt.
        theme: Visual theme name ("normal" or "gothic").
        state: Application state to mutate in-place.
    """
    maze, path = _build_maze(config)
    tile = _tile_size_for_window(maze)
    generate_all_assets(tile)
    assets = Assets(mlx, mlx_ptr, tile, theme)

    state.maze = maze
    state.path = path
    state.tile_size = tile
    state.assets = assets
    state.theme = theme
    state.scene = "maze"
    state.show_path = True
    state.needs_redraw = True


# ── Entry point ───────────────────────────────────────────

def run_app(config: dict[str, Any]) -> None:
    """
    Open the MLX window and run the full application loop.

    Shows a theme-selection menu first; transitions to the maze
    in the same window using the parsed config from config.txt.

    Args:
        config: Parsed and validated config dict.
    """
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    win_ptr = mlx.mlx_new_window(
        mlx_ptr, WINDOW_WIDTH, WINDOW_HEIGHT, "A-MAZE-ING"
    )

    state = AppState()
    state.menu_imgs = _prepare_menu_images(mlx, mlx_ptr)

    def on_close(param: Any) -> None:
        """Quit on window-close event."""
        os._exit(0)

    def on_key(key: int, param: Any) -> None:
        """Handle key input for both menu and maze scenes."""
        if key == KEY_ESC:
            os._exit(0)
        if state.scene == "menu":
            theme: str | None = None
            if key == KEY_1:
                theme = THEME_LIGHT
            elif key == KEY_2:
                theme = THEME_DARK
            if theme is not None:
                try:
                    _transition_to_maze(
                        mlx, mlx_ptr,
                        config, theme, state,
                    )
                except Exception as err:
                    print(f"Error generating maze: {err}")

    def on_loop(param: Any) -> None:
        """Redraw the window when the dirty flag is set."""
        if not state.needs_redraw:
            return
        mlx.mlx_clear_window(mlx_ptr, win_ptr)
        if state.scene == "menu":
            _draw_menu(mlx, mlx_ptr, win_ptr, state)
        elif (
            state.scene == "maze"
            and state.maze is not None
            and state.assets is not None
        ):
            path_arg = (
                state.path
                if state.show_path and state.path
                else None
            )
            draw_maze(
                state.maze, mlx, mlx_ptr, win_ptr,
                state.tile_size, state.assets,
                state.maze.grid, path_arg,
            )
        state.needs_redraw = False

    def on_expose(param: Any) -> None:
        """Force a redraw whenever the window is exposed."""
        state.needs_redraw = True

    mlx.mlx_hook(win_ptr, 33, 0, on_close, None)
    mlx.mlx_key_hook(win_ptr, on_key, None)
    mlx.mlx_expose_hook(win_ptr, on_expose, None)
    mlx.mlx_loop_hook(mlx_ptr, on_loop, None)
    mlx.mlx_loop(mlx_ptr)
