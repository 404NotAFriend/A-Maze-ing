from mazegen.Maze import Maze
from utils.hex_utils import maze_to_hex
from utils.path_utils import path_to_directions


def export_maze(maze: Maze,
                path: list[tuple[int, int]],
                output_file: str) -> None:
    """
    Creates the file maze.txt with the following information:
    -> Hex Values (from hex_utils)
    -> Entry and Exit points (given by the config.txt file)
    -> NSWE Coordinates from the path solver algorithm
    Obs. This file must be rewritten from the start
    everytime the program restarts
    """

    # Hex values from each logical cell
    hex_values = maze_to_hex(maze)

    # ENTRY / EXIT Values
    entry_y, entry_x = maze.entry
    exit_y, exit_x = maze.exit

    # N E S W directions made from the path solver
    dir_path = path_to_directions(path)

    with open(output_file, "w") as file:
        for line in hex_values:
            file.write("".join(line) + "\n")
        file.write(f"\n{entry_y},{entry_x}\n")
        file.write(f"{exit_y},{exit_x}\n")
        file.write("".join(dir_path) + "\n")


def print_maze_file(output_file: str) -> None:
    """
    After the previous functions export_maze
    has created the file and uploaded all the information needed,
    this function will then read its content
    """
    try:
        with open(output_file, "r") as file:
            for line in file:
                print(line, end="")
    except (FileNotFoundError, PermissionError, Exception) as e:
        print(f"print_maze_file() failed -> {e}")
