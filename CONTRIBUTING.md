# Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change.

## Development setup

```bash
git clone <repo-url>
cd <repo-name>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # if present
```

## Running tests

```bash
pytest -v
```

## Code style

- Follow PEP 8.
- Use type hints.
- Add docstrings for public functions and classes.
- Keep functions small and focused.

## Pull request process

1. Create a feature branch.
2. Add tests for any new functionality.
3. Ensure all tests pass and lint is clean.
4. Update the README if you change public behavior.
5. Open a PR with a clear description of the change.
