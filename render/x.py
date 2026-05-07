

from mlx import Mlx
from render.resize import generate_all_assets
from render.Assets import Assets
import os


def close(param):
    """Close / exit the program"""
    os._exit(0)


def key_hook(key, param):
    """Exit with ESC"""
    if key == 65307:
        os._exit(0)


def mlx_window():
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    win_ptr = mlx.mlx_new_window(mlx_ptr, 1650, 1350, "A_ma_ing")

    mlx.mlx_hook(win_ptr, 33, 0, close, None)
    mlx.mlx_key_hook(win_ptr, key_hook, None)

    assets = Assets(mlx, mlx_ptr, 32)
    print(assets.wall)
    

    # Generate the images and convert to xpm
    generate_all_assets(32)

    # BANNER
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr,
                                assets.banner, 65, 40)

    mlx.mlx_loop(mlx_ptr)
