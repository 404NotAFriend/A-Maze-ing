"""Menu scene for A-Maze-ing — plug-and-play over any project."""
from __future__ import annotations

import os
import sys
import subprocess
from dataclasses import dataclass
from typing import Any

from PIL import Image  # type: ignore
from mlx import Mlx  # type: ignore

from mazegen.Maze import Maze
from render.mlx_renderer import mlx_window


# ── Window ────────────────────────────────────────────────
WINDOW_WIDTH: int = 1600
WINDOW_HEIGHT: int = 900

# ── Key codes ─────────────────────────────────────────────
KEY_ESC: int = 65307
KEY_1: int = 49
KEY_2: int = 50


@dataclass
class MenuImages:
    """Pre-loaded MLX image pointer for the menu background."""

    bg: Any = None


# ── Asset helpers ─────────────────────────────────────────

def _prepare_menu_images(mlx: Mlx, mlx_ptr: Any) -> MenuImages:
    """Load the menu background XPM, generating it from PNG if needed."""
    os.makedirs("assets/generated", exist_ok=True)
    imgs = MenuImages()

    bg_xpm = (
        f"assets/generated/"
        f"menu_bgnew_{WINDOW_WIDTH}x{WINDOW_HEIGHT}.xpm"
    )
    if not os.path.exists(bg_xpm):
        bg_png = bg_xpm.replace(".xpm", ".png")
        if not os.path.exists(bg_png):
            src = Image.open("assets/imgs/menu_backgroundnew.png")
            src = src.resize(
                (WINDOW_WIDTH, WINDOW_HEIGHT), Image.LANCZOS
            )
            src.save(bg_png)
        os.system(f"magick {bg_png} {bg_xpm}")
    imgs.bg, _, _ = mlx.mlx_xpm_file_to_image(mlx_ptr, bg_xpm)

    return imgs


# ── Menu rendering ────────────────────────────────────────

def _draw_menu(
    mlx: Mlx, mlx_ptr: Any, win_ptr: Any, imgs: MenuImages
) -> None:
    """Render the menu background image."""
    if imgs.bg is None:
        return
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, imgs.bg, 0, 0)


# ── Standalone menu (runs in its own process) ─────────────

def run_menu_only() -> None:
    """
    Standalone menu entry point — always runs in its own process.
    Exits with code: 1 = normal theme, 2 = gothic theme, 0 = quit.
    """
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    win_ptr = mlx.mlx_new_window(
        mlx_ptr, WINDOW_WIDTH, WINDOW_HEIGHT, "A-MAZE-ING"
    )

    menu_imgs = _prepare_menu_images(mlx, mlx_ptr)
    needs_redraw = True

    def on_close(param: Any) -> None:
        os._exit(0)

    def on_key(key: int, param: Any) -> None:
        if key == KEY_ESC:
            os._exit(0)
        elif key == KEY_1:
            os._exit(1)
        elif key == KEY_2:
            os._exit(2)

    def on_loop(param: Any) -> None:
        nonlocal needs_redraw
        if not needs_redraw:
            return
        mlx.mlx_clear_window(mlx_ptr, win_ptr)
        _draw_menu(mlx, mlx_ptr, win_ptr, menu_imgs)
        needs_redraw = False

    def on_expose(param: Any) -> None:
        nonlocal needs_redraw
        needs_redraw = True

    mlx.mlx_hook(win_ptr, 33, 0, on_close, None)
    mlx.mlx_key_hook(win_ptr, on_key, None)
    mlx.mlx_expose_hook(win_ptr, on_expose, None)
    mlx.mlx_loop_hook(mlx_ptr, on_loop, None)
    mlx.mlx_loop(mlx_ptr)


# ── Public API (called from a_maze_ing.py) ────────────────

def run_app(maze: Maze, path: list[tuple[int, int]]) -> None:
    """
    Show the theme-selection menu, then launch the maze.

    The menu runs in a subprocess so it has its own clean MLX
    connection. When the user picks a theme the subprocess exits
    with a code and the main process calls mlx_window normally —
    exactly the same path Sara's project takes.
    """
    result = subprocess.run([sys.executable, "-m", "render.menu"])

    if result.returncode == 1:
        mlx_window(maze, path, "normal")
    elif result.returncode == 2:
        mlx_window(maze, path, "gothic")


# ── Module entry point ────────────────────────────────────

if __name__ == "__main__":
    run_menu_only()
