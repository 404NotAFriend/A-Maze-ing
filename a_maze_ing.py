from mazegen.MazeGenerator import MazeGenerator
from parsing.config_parser import parse_config, get_config_path, convert_config
# from utils.export_utils import print_maze_file

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
        mazegen.generate_maze()
        mazegen.solve("bfs")
        mazegen.render(show_path=True)
        if not mazegen.logo_pos:
            print("The maze was not big enough to showcase the maze logo.")
            # time.sleep(1)
        mazegen.export(config["OUTPUT_FILE"])
        # print_maze_file(config["OUTPUT_FILE"])
    except Exception as e:
        print(f"Error: {e}")
