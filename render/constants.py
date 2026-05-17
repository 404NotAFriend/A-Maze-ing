# ── Window ────────────────────────────────────────────────
WINDOW_WIDTH: int = 1600
WINDOW_HEIGHT: int = 900

# ── Banner ────────────────────────────────────────────────
BANNER_HEIGHT: int = 120
BANNER_PADDING_V: int = 5
BANNER_PADDING_H: int = 200

BANNER_WIDTH: int = WINDOW_WIDTH - (BANNER_PADDING_H * 2)
BANNER_X: int = BANNER_PADDING_H
BANNER_Y: int = WINDOW_HEIGHT - BANNER_HEIGHT - BANNER_PADDING_V

# ── Maze area ─────────────────────────────────────────────
MAZE_AREA_HEIGHT: int = BANNER_Y - 5
MAZE_AREA_WIDTH: int = WINDOW_WIDTH


# ── Maze centering ────────────────────────────────────────
def maze_offset_x(grid_width: int, tile_size: int) -> int:
    """Center maze horizontally"""
    return max(0, (MAZE_AREA_WIDTH - grid_width * tile_size) // 2)


def maze_offset_y(grid_height: int, tile_size: int) -> int:
    """Align maze to bottom of maze area (close to banner)"""
    return max(0, MAZE_AREA_HEIGHT - grid_height * tile_size)
