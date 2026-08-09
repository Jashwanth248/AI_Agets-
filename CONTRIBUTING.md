# Contributing

Thanks for considering a contribution! This project follows a simple workflow.

## Setup

```bash
git clone https://github.com/Jashwanth248/AI_Agets-.git
cd AI_Agets-
python -m venv .venv && source .venv/bin/activate
make install-dev
```

## Development workflow

1. Create a branch: `git checkout -b feature/my-change`
2. Make your change, with tests where it makes sense (see `tests/`)
3. Run the checks locally before opening a PR:
   ```bash
   make format
   make lint
   make test
   ```
4. Open a pull request against `main`. CI (`.github/workflows/ci.yml`) runs lint, tests, evaluation, and a Docker build.

## Adding a new agent

Keep deterministic logic free of model/API dependencies where possible so it can be unit-tested without a live model or API key.

## Evaluation

If you change a prompt or model, run:

```bash
make eval
```

Add regression cases to `evaluation/golden_dataset.jsonl` when fixing behavior.

## Code style

- Formatted with `black`, linted with `ruff`
- Type hints on new functions where practical
- Docstrings on public functions/classes
