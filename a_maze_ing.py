from parsing.config_parser import get_config_path, parse_config, convert_config
from render.menu import run_app


if __name__ == "__main__":
    try:
        config_path = get_config_path()
        config = parse_config(config_path)
        config = convert_config(config)
        run_app(config)
    except Exception as e:
        print(f"Error: {e}")
