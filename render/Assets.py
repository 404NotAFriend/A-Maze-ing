from mlx import Mlx
from typing import Any


class Assets:
    """
    Loads and stores all game assets
    """
    def __init__(self, mlx: Mlx, mlx_ptr: Any, tile_size: int) -> None:
        # MENU BACKGROUND
        self.title_size = tile_size
        self.menu_background, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            "assets/imgs/menu_background.xpm"
        )

        # NORMAL THEME
        self.wall, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            f"assets/generated/wall_{tile_size}.xpm"
        )

        self.floor_normal, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            f"assets/generated/normal_floor_{tile_size}.xpm"
        )

        # GOTHIC THEME
        self.floor_gothic, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            f"assets/generated/gothic_floor_{tile_size}.xpm"
        )

        # UI HUD / BANNER
        self.banner, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            "assets/imgs/banner.xpm"
        )

        # DUCKS / PLAYER
        self.duck_normal, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            f"assets/generated/normal_duck_{tile_size}.xpm"
        )

        self.duck_gothic, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            f"assets/generated/gothic_duck_{tile_size}.xpm"
        )
