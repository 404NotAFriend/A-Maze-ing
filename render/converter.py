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
        f"magick {png_path} {xpm_path}"
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

    resized_light_wall_png = (
        f"assets/generated/light_wall_{tile_size}.jpeg"
    )

    light_wall_xpm = (
        f"assets/generated/light_wall_{tile_size}.xpm"
    )

    if not os.path.exists(light_wall_xpm):

        generate_scaled_asset(
            "assets/imgs/light_wall.png",
            resized_light_wall_png,
            tile_size
        )

        convert_to_xpm(
            resized_light_wall_png,
            light_wall_xpm
        )

    # -------------------------

    resized_dark_42_png = (
        f"assets/generated/dark_wall_{tile_size}.png"
    )

    wall_dark_42_42_xpm = (
        f"assets/generated/dark_wall_{tile_size}.xpm"
    )

    if not os.path.exists(wall_dark_42_42_xpm):

        generate_scaled_asset(
            "assets/imgs/dark_wall.png",
            resized_dark_42_png,
            tile_size
        )

        convert_to_xpm(
            resized_dark_42_png,
            wall_dark_42_42_xpm
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

    if not os.path.exists(normal_floor_xpm):

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

    if not os.path.exists(gothic_floor_xpm):

        generate_scaled_asset(
            "assets/imgs/gothic_floor.png",
            resized_gothic_floor_png,
            tile_size
        )

        convert_to_xpm(
            resized_gothic_floor_png,
            gothic_floor_xpm
        )

    # -------------------------
    # TRAIL
    # -------------------------

    normal_trail_png = (
        f"assets/generated/normal_trail_{tile_size}.png"
    )

    normal_trail_xpm = (
        f"assets/generated/normal_trail_{tile_size}.xpm"
    )

    if not os.path.exists(normal_trail_xpm):

        generate_scaled_asset(
            "assets/imgs/normal_trail.png",
            normal_trail_png,
            tile_size
        )

        convert_to_xpm(
            normal_trail_png,
            normal_trail_xpm
        )
    
    # -------------------------

    gothic_trail_png = (
        f"assets/generated/gothic_trail_{tile_size}.png"
    )

    gothic_trail_xpm = (
        f"assets/generated/gothic_trail_{tile_size}.xpm"
    )

    if not os.path.exists(gothic_trail_xpm):

        generate_scaled_asset(
            "assets/imgs/gothic_trail.png",
            gothic_trail_png,
            tile_size
        )

        convert_to_xpm(
            gothic_trail_png,
            gothic_trail_xpm
        )

    # -------------------------
    # DUCK
    # -------------------------

    resized_normal_duck_png = (
        f"assets/generated/normal_duck_{tile_size}.png"
    )

    normal_duck_xpm = (
        f"assets/generated/normal_duck_{tile_size}.xpm"
    )

    if not os.path.exists(normal_duck_xpm):

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

    if not os.path.exists(gothic_duck_xpm):

        generate_scaled_asset(
            "assets/imgs/gothic_duck.png",
            resized_gothic_duck_png,
            tile_size
        )

        convert_to_xpm(
            resized_gothic_duck_png,
            gothic_duck_xpm
        )
