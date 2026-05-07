from PIL import Image
import os


def generate_scaled_asset(
    input_path: str,
    output_path: str,
    tile_size: int
) -> None:
    """
    Resize image and save as PNG
    """

    # Open original image
    image = Image.open(input_path)

    # Resize image
    image = image.resize(
        (tile_size, tile_size),
        Image.NEAREST
    )

    # Save resized PNG
    image.save(output_path)


def convert_to_xpm(
    png_path: str,
    xpm_path: str
) -> None:
    """
    Convert PNG -> XPM using ImageMagick
    """

    os.system(
        f"convert {png_path} {xpm_path}"
    )


def generate_all_assets(
    tile_size: int
) -> None:
    """
    Generate all resized assets
    """

    os.makedirs(
        "assets/generated",
        exist_ok=True
    )

    # -------------------------
    # WALL
    # -------------------------

    resized_wall_png = (
        f"assets/generated/wall_{tile_size}.png"
    )

    wall_xpm = (
        f"assets/generated/wall_{tile_size}.xpm"
    )

    generate_scaled_asset(
        "assets/imgs/walls.jpeg",
        resized_wall_png,
        tile_size
    )

    convert_to_xpm(
        resized_wall_png,
        wall_xpm
    )

    # -------------------------
    # FLOOR
    # -------------------------

    resized_normal_floor_png = (
        f"assets/generated/normal_floor_{tile_size}.png"
    )

    normal_floor_xpm = (
        f"assets/generated/normal_floor_{tile_size}.xpm"
    )

    generate_scaled_asset(
        "assets/imgs/normal_floor.jpeg",
        resized_normal_floor_png,
        tile_size
    )

    convert_to_xpm(
        resized_normal_floor_png,
        normal_floor_xpm
    )

    # --------------------------

    resized_gothic_floor_png = (
        f"assets/generated/gothic_floor_{tile_size}.png"
    )

    gothic_floor_xpm = (
        f"assets/generated/gothic_floor_{tile_size}.xpm"
    )

    generate_scaled_asset(
        "assets/imgs/gothic_floor.jpeg",
        resized_gothic_floor_png,
        tile_size
    )

    convert_to_xpm(
        resized_gothic_floor_png,
        gothic_floor_xpm
    )

    # -------------------------
    # DUCK
    # -------------------------

    resized_normal_duck_png = (
        f"assets/generated/duck_{tile_size}.png"
    )

    normal_duck_xpm = (
        f"assets/generated/duck_{tile_size}.xpm"
    )

    generate_scaled_asset(
        "assets/imgs/normal_duck.jpeg",
        resized_normal_duck_png,
        tile_size
    )

    convert_to_xpm(
        resized_normal_duck_png,
        normal_duck_xpm
    )

    # --------------------------

    resized_gothic_duck_png = (
        f"assets/generated/gothic_duck_{tile_size}.png"
    )

    gothic_duck_xpm = (
        f"assets/generated/gothic_duck_{tile_size}.xpm"
    )

    generate_scaled_asset(
        "assets/imgs/gothic_duck.jpeg",
        resized_gothic_duck_png,
        tile_size
    )

    convert_to_xpm(
        resized_gothic_duck_png,
        gothic_duck_xpm
    )
