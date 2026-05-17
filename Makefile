NAME = a_maze_ing.py
PYTHON = python3
VENV = venv
PIP = $(VENV)/bin/python3 -m pip

all: run

# INSTALL VENV
venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating venv..."; \
		$(PYTHON) -m venv $(VENV); \
	else \
		echo "Venv already exists"; \
	echo "To activate, Run the following command:"; \
	echo "source $(VENV)/bin/activate"; \
	fi

# INSTALL ALL REQUIREMENTS

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

	#Bruno -> Install MLX library from project's .whl file
	@if [ -f "mlx_CLXV/mlx-2.2-py3-none-any.whl" ]; then \
		$(PIP) install mlx_CLXV/mlx-2.2-py3-none-any.whl; \
	else \
		echo "Building MLX library..."; \
		cd mlx_CLXV && make && cd ..; \
		$(PIP) install mlx_CLXV/mlx-2.2-py3-none-any.whl; \
	fi

	@if [ -f "$$HOME/.linuxbrew/bin/brew" ]; then \
		eval "$$($$HOME/.linuxbrew/bin/brew shellenv)"; \
	fi; \
	if ! command -v magick >/dev/null 2>&1; then \
		echo "ImageMagick not found"; \
		echo "Checking local Homebrew..."; \
		if [ ! -f "$$HOME/.linuxbrew/bin/brew" ]; then \
			echo "Local Homebrew not found"; \
			echo "Installing Homebrew locally..."; \
			mkdir -p $$HOME/.linuxbrew; \
			git clone https://github.com/Homebrew/brew.git $$HOME/.linuxbrew; \
		fi; \
		echo "Setting up Homebrew environment..."; \
		eval "$$($$HOME/.linuxbrew/bin/brew shellenv)"; \
		echo "Installing ImageMagick..."; \
		$$HOME/.linuxbrew/bin/brew install imagemagick; \
	else \
		echo "ImageMagick already installed"; \
	fi

# RUN THE GAME
run:
	@if [ -f "$$HOME/.linuxbrew/bin/brew" ]; then \
		eval "$$($$HOME/.linuxbrew/bin/brew shellenv)" && $(VENV)/bin/python3 $(NAME) config.txt; \
	else \
		$(VENV)/bin/python3 $(NAME) config.txt; \
	fi

# DEBUGGER
debug:
	@if [ -f "$$HOME/.linuxbrew/bin/brew" ]; then \
		eval "$$($$HOME/.linuxbrew/bin/brew shellenv)" && $(VENV)/bin/python3 -m pdb $(NAME) config.txt; \
	else \
		$(VENV)/bin/python3 -m pdb $(NAME) config.txt; \
	fi

# CHECK FOR NORM ERRORS
lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . \
		--strict

# CLEANERS
clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf .mypy_cache
	rm -f assets/generated/*

fclean: clean
	rm -rf $(VENV)

re: fclean install

.PHONY: all venv install run debug lint clean fclean re
