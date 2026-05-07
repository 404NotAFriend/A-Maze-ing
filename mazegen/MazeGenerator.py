import random
import time
import os
from mazegen.Maze import Maze
from mazegen.solver import bfs_solve_maze
from mazegen.generator import (dfs_generator,
                               apply_entry_exit,
                               check_open_areas,
                               break_walls,
                               add_42_logo)
from render.ascii_renderer import render_ascii
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

                path = bfs_solve_maze(maze)
                if path:
                    self.logo_pos = logo_pos
                    self.maze = maze
                    return maze
            raise ValueError("generate_maze(): Could not generate "
                             "a valid maze.")

        except (KeyError, Exception) as e:
            raise ValueError(f"generate_maze(): {e}")

    def solve(self, algorithm: str) -> list[tuple[int, int]]:
        """
        Checks for the algorithm to apply,
        and uses it to solve the maze
        """
        if algorithm == "bfs":
            path = bfs_solve_maze(self.maze)
        else:
            raise ValueError("solve(): No algorithm found with that name.")
        self.path = path
        return path

    def render(self, show_path: bool) -> None:
        """
        Renders the maze and shows it on the terminal
        """
        try:
            if not show_path:
                render_ascii(self.maze.grid, self.maze)

            else:
                for i in range(1, len(self.path) + 1):
                    os.system("clear")
                    render_ascii(self.maze.grid, self.maze, self.path[:i])
                    time.sleep(0.05)
        except Exception:
            print("render(): Failed to show the maze.")

    def export(self, output_file: str) -> None:
        """
        Exports the information from the maze to
        the output_maze.txt file
        """
        export_maze(self.maze, self.path, output_file)
