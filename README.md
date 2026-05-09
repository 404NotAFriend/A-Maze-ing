# 🐍 Virtual Environment: Instructions

Short guide to create an isolated Python environment, install project dependencies, and manage activation/deactivation both on windows and linux.

### Create
```bash
python3 -m venv venv
```

### Activate
```bash
source venv/bin/activate
```

## Install requirements (on venv)
```bash
pip install -r requirements.txt
```

## Deactivate
```bash
deactivate
```

## Run main - Example
```bash
 python3 a_maze_ing.py config.txt
```

## Install MinilibMLX and check man (on venv)
```bash
python3 -m pip install ./mlx-2.2-py3-ubuntu-any.whl
man -M mlx_CLXV/man mlx
```

## Install Lib Pil and Convert (on venv)
```bash
pip install pillow
git clone <brew>
brew install magick
```

## 📦 Config Parser (parsing/config_parser.py)

#### Features:

- Reads the configuration file  
- Ignores empty lines and comments  
- Validates line format (`KEY=VALUE`)  
- Detects duplicate keys  
- Ensures all mandatory required keys are present  
- Displays clear error messages when needed  
- Converts configuration values into appropriate types (int, tuple, bool)  
- Validates values to ensure the maze can be generated correctly  

---

## 🧱 Maze (core/maze.py)

#### Features:

- Stores the maze structure and core data  
- Initializes a fully walled grid (default state)  
- Expands logical maze into a grid with walls (`2 * size + 1`)  
- Stores entry and exit coordinates  
- Provides a base structure for generation algorithms  

---

## 🌱 Maze Generator (core/generator.py)

#### Features:

- Generates a maze using the Depth-First Search (DFS) algorithm  
- Ensures all cells are reachable (full connectivity)  
- Randomizes directions to produce different maze layouts  
- Breaks walls between cells to create valid paths  
- Applies entry and exit openings on maze borders  
- Validates entry and exit positions before opening them  

---

## 🖨️ ASCII Renderer (render/ascii_renderer.py)

#### Features:

- Displays the maze in the terminal  
- Converts internal grid values into visual symbols  
- Distinguishes walls and paths (`■` / `□`)  
- Provides a simple visual representation for debugging and testing  

---

## 🚀 Main (a_maze_ing.py)

#### Features:

- Entry point of the application  
- Loads and validates configuration  
- Initializes the maze structure  
- Runs the maze generation process  
- Applies entry and exit openings  
- Renders the maze in the terminal  
- Handles errors gracefully without crashing  


## 📦 Next steps

- def solve_maze(maze: Maze) -> list[tuple[int, int]]
    Algorithm to solve the path
- def path_to_directions(path: list[tuple[int, int]]) -> str
    Converte the path into directions (W, E, S, N)
    To later add them in the maze.txt
- def maze_to_hex(maze: Maze) -> list[list[str]]
    Converte the maze to hex
- def export_maze(maze: Maze, hex_grid: list[list[str], path_str[str]]) -> None
    Export the maze (maze.txt)
...
Pos: Design / graphs, add 42 logo, unperfect_path (when perfect=false), verify maze conditions (open sizes, etc)

config
  ↓
Maze()
  ↓
dfs_generator()
  ↓
apply_entry_exit()
  ↓
check_open_areas()
  ↓
add_42_logo()   
  ↓
if not PERFECT:
    break_walls()    
  ↓
solve_maze()         
  ↓
path_to_directions() 
  ↓
maze_to_hex()        
  ↓
export_maze()
  ↓
render()
  ↓
menu()               
  ↓
Design Duck (easy / hard mode; commands to play instead of using the maze solver algorithm) 