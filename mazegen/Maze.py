class Maze:
    """
    Stores the maze data
    This is TEMPORARY with 0 or 1 int values - for tests
    """
    def __init__(self,
                 width: int,
                 height: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int]) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit

        self.grid: list[list[int]] = []
        # Size of the grid with walls:
        self.grid_height = 2 * height + 1
        self.grid_width = 2 * width + 1

        for _ in range(0, self.grid_height):
            row: list[int] = []
            for _ in range(0, self.grid_width):
                row.append(1)
            self.grid.append(row)
