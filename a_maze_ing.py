from mazegen.MazeGenerator import MazeGenerator
from parsing.config_parser import parse_config, get_config_path, convert_config
from render.menu import run_app


if __name__ == "__main__":
    try:
        config = parse_config(get_config_path())
        config = convert_config(config)

        mazegen = MazeGenerator(config["WIDTH"],
                                config["HEIGHT"],
                                config["ENTRY"],
                                config["EXIT"],
                                config["PERFECT"],
                                config.get("SEED"))
        maze = mazegen.generate_maze()
        path = mazegen.solve("bfs")
        mazegen.export(config["OUTPUT_FILE"])

        run_app(maze, path)
    except Exception as e:
        print(f"Error: {e}")
