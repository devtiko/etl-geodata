# Agent notes

- Python 3.12+ project managed with `uv`; install/sync with `uv sync`.
- CLI entrypoint is `etl.main:main` (`uv run etl`). Use `uv run etl --state 31` for a bounded run; no `--state` processes all 32 states and their municipalities/localities and makes many live INEGI requests. `--refresh` bypasses the request cache.
- ETL flow is composed in `src/etl/main.py`: `extract/` calls and caches INEGI data, `transform/` merges geography and geometry, `load/` persists outputs, and `pipelines/` orchestrates it. CLI parsing is in `src/etl/cli.py`; shared storage/cache are in `shared/`.
- Runtime paths are relative to the current working directory (`Settings.DATA_DIR = Path("data")`). `data/` is gitignored and contains both downloaded raw files and processed outputs; `data/requests.json` is the persistent request cache. Avoid deleting or rewriting it unless a data refresh/reset is intended.
- Run tests with `uv run pytest`; there is currently no `tests/` directory or configured lint/format task. `pyproject.toml` has basedpyright settings but does not declare it as a project dependency.
- INEGI locality queries require both state and municipality keys; tabular and GeoJSON locality responses may not have one-to-one records. See `docs/research.md` before changing endpoint assumptions or merge behavior.
