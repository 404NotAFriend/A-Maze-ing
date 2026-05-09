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
	fi

# ENTER ON VENV / ACTIVATE
activate:
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "Already inside a virtual environment"; \
	else \
		echo "Run:"; \
		echo "source $(VENV)/bin/activate"; \
	fi

# INSTALL ALL REQUIREMENTS

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

	@if ! command -v convert >/dev/null 2>&1; then \
		echo "ImageMagick not found"; \
		echo "Checking Homebrew..."; \
		if ! command -v brew >/dev/null 2>&1; then \
			echo "Homebrew not found"; \
			echo "Installing Homebrew..."; \
			/bin/bash -c "$$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"; \
			eval "$$($$HOME/.linuxbrew/bin/brew shellenv)" || true; \
			eval "$$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)" || true; \
		fi; \
		echo "Installing ImageMagick..."; \
		brew install imagemagick; \
	else \
		echo "ImageMagick already installed"; \
	fi

# RUN THE GAME
run:
	$(VENV)/bin/python3 $(NAME) config.txt

# DEBUGGER
debug:
	$(VENV)/bin/python3 -m pdb $(NAME) config.txt

# CHECK FOR NORM ERRORS 
lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

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
