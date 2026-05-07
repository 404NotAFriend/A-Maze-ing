NAME = a_maze_ing.py
PYTHON = python3
VENV = venv
PIP = $(VENV)/bin/python3 -m pip

all: run

venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating venv..."; \
		$(PYTHON) -m venv $(VENV); \
	else \
		echo "Venv already exists"; \
	fi

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(VENV)/bin/python3 $(NAME) config.txt

debug:
	$(VENV)/bin/python3 -m pdb $(NAME) config.txt

lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf .mypy_cache

fclean: clean
	rm -rf $(VENV)

re: fclean install

.PHONY: all venv install run debug lint clean fclean re
