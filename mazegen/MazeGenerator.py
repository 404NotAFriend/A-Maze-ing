import random
from mazegen.Maze import Maze
from mazegen.solver import bfs_solve_maze
from mazegen.generator import (dfs_generator,
                               apply_entry_exit,
                               check_open_areas,
                               break_walls,
                               add_42_logo)
from utils.export_utils import export_maze


class MazeGenerator:
    """
    Calls all needed functions to generate the maze:
    dfs to create a random perfect path
    adds the entry and exit cells
    if the maze is not perfect, then it "breaks walls"
    to create extra paths
    Calls the algorithm to solve and show the solution
    exports the info to the output_maze.txt file
    """
    def __init__(self,
                 width: int,
                 height: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int],
                 perfect: bool,
                 seed: int | None) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed

    def generate_maze(self) -> Maze:
        """
        Generate a maze with dfs
        Check if all conditions apply with check_open_areas
        If not, generate another maze
        Add the entry and exit cells
        """
        try:
            if self.seed is not None:
                random.seed(self.seed)

            max_attempts = 1000

            for _ in range(max_attempts):
                maze = Maze(
                    self.width,
                    self.height,
                    self.entry,
                    self.exit
                )

                dfs_generator(maze)
                apply_entry_exit(maze)

                if not check_open_areas(maze):
                    continue

                logo_pos = add_42_logo(maze)
                if not logo_pos:
                    print("The maze was not big enough "
                          "to showcase the maze logo.")

                if not self.perfect:
                    break_walls(maze, logo_pos)

                path, _ = bfs_solve_maze(maze)
                if path:
                    self.logo_pos = logo_pos
                    self.maze = maze
                    return maze
            raise ValueError("generate_maze(): Could not generate "
                             "a valid maze.")

        except (KeyError, Exception) as e:
            raise ValueError(f"generate_maze(): {e}")

    def solve(self, algorithm: str) -> tuple[list[tuple[int, int]],
                                             list[tuple[int, int]]]:
        """
        Checks for the algorithm to apply,
        and uses it to solve the maze
        """
        if algorithm == "bfs":
            path, explored = bfs_solve_maze(self.maze)
        else:
            raise ValueError("solve(): No algorithm found with that name.")
        self.path = path
        self.explored = explored
        return path, explored

    def export(self, output_file: str) -> None:
        """
        Exports the information from the maze to
        the output_maze.txt file
        """
        export_maze(self.maze, self.path, output_file)
