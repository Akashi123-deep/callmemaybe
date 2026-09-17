UV = uv run
SRC = python -m src
MYPYFLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --follow-imports=skip

install: 
	uv sync

run:
	@$(UV) $(SRC)

debug:
	@$(UV) python -m pdb -m src

lint:
	@$(UV) flake8 src && $(UV) mypy src $(MYPYFLAGS)

clean: