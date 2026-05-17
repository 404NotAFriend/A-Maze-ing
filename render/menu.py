from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Any
from PIL import Image
from mlx import Mlx
from render.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BANNER_HEIGHT,
    BANNER_WIDTH,
    BANNER_X,
    BANNER_Y
)

# ── Key codes ─────────────────────────────────────────────
KEY_ESC: int = 65307
KEY_1: int = 49
KEY_2: int = 50


@dataclass
class MenuImages:
    """Pre-loaded MLX image pointers for menu background and banner."""
    bg: Any = None
    banner: Any = None


# ── Asset helpers ─────────────────────────────────────────
def _prepare_menu_images(mlx: Mlx, mlx_ptr: Any) -> MenuImages:
    """Load the menu background and banner XPMs,
    generating them from PNG if needed."""
    os.makedirs("assets/generated", exist_ok=True)
    imgs = MenuImages()

    # ── Background ────────────────────────────────────────
    bg_xpm = (
        f"assets/generated/"
        f"menu_bgnew_{WINDOW_WIDTH}x{WINDOW_HEIGHT}.xpm"
    )
    if not os.path.exists(bg_xpm):
        bg_png = bg_xpm.replace(".xpm", ".png")
        if not os.path.exists(bg_png):
            src = Image.open("assets/imgs/menu_background.png")
            resized_src = src.resize(
                (WINDOW_WIDTH, WINDOW_HEIGHT),
                Image.Resampling.LANCZOS
            )
            resized_src.save(bg_png)
        os.system(f"magick {bg_png} {bg_xpm}")
    imgs.bg, _, _ = mlx.mlx_xpm_file_to_image(mlx_ptr, bg_xpm)

    # ── Banner ────────────────────────────────────────────
    banner_xpm = (
        f"assets/generated/"
        f"banner_{BANNER_WIDTH}x{BANNER_HEIGHT}.xpm"
    )
    if not os.path.exists(banner_xpm):
        banner_png = banner_xpm.replace(".xpm", ".png")
        if not os.path.exists(banner_png):
            src = Image.open("assets/imgs/banner.png")

            # Convert palette image to RGBA to handle transparency
            src_rgba = src.convert("RGBA")

            # Crop to non-transparent content bounds (removes black gaps)
            bbox = src_rgba.getbbox()
            if bbox:
                src_rgba = src_rgba.crop(bbox)

            # Composite onto black background to remove colored bg
            background = Image.new("RGB", src_rgba.size, (0, 0, 0))
            background.paste(src_rgba, mask=src_rgba.split()[3])

            # Resize to banner dimensions
            resized = background.resize(
                (BANNER_WIDTH, BANNER_HEIGHT),
                Image.Resampling.LANCZOS
            )
            resized.save(banner_png)
        os.system(f"magick {banner_png} {banner_xpm}")
    imgs.banner, _, _ = mlx.mlx_xpm_file_to_image(mlx_ptr, banner_xpm)

    return imgs


# ── Menu rendering ────────────────────────────────────────
def _draw_menu(
    mlx: Mlx, mlx_ptr: Any, win_ptr: Any, imgs: MenuImages
) -> None:
    """Render the menu background image."""
    if imgs.bg is None:
        return
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, imgs.bg, 0, 0)


def _draw_banner(
    mlx: Mlx, mlx_ptr: Any, win_ptr: Any, imgs: MenuImages
) -> None:
    """Render the banner centered with padding."""
    if imgs.banner is None:
        return
    mlx.mlx_put_image_to_window(
        mlx_ptr, win_ptr, imgs.banner, BANNER_X, BANNER_Y
    )
