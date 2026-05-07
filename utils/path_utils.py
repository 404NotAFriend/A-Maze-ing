def path_to_directions(path: list[tuple[int, int]]) -> list[str]:
    """
    Receives the path from the path solver algorithm
    And converts each move to a str list with: N, E, S, W values
    """
    path_str: list[str] = []

    for i in range(len(path) - 1):
        (y, x) = path[i]
        (dy, dx) = path[i + 1]

        if dy < y:
            path_str.append("N")  # UP
        elif dy > y:
            path_str.append("S")  # DOWN
        elif dx < x:
            path_str.append("W")  # LEFT
        elif dx > x:
            path_str.append("E")  # RIGHT
    return path_str
