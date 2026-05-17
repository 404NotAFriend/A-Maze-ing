from mazegen.MazeGenerator import MazeGenerator
from parsing.config_parser import parse_config, get_config_path, convert_config
from render.mlx_renderer import mlx_window
from render.GameState import GameState


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
        path, explored = mazegen.solve("bfs")

        game = GameState()
        game.maze = maze
        game.path = path
        game.explored = explored
        game.generator = mazegen
        game.output_file = config["OUTPUT_FILE"]

        mlx_window(game)

    except Exception as e:
        print(f"Error: {e}")
