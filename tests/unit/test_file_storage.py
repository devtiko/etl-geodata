import json
from pathlib import Path

from etl.shared.file_storage import FileStorage


def test_read_json_returns_default_when_file_is_missing(tmp_path: Path) -> None:
  default = {"fallback": True}

  assert FileStorage().read_json(tmp_path / "missing.json", default=default) == default


def test_read_json_returns_none_for_invalid_json(tmp_path: Path) -> None:
  path = tmp_path / "invalid.json"
  path.write_text("{invalid", encoding="utf-8")

  assert FileStorage().read_json(path) is None


def test_write_json_creates_parent_directories_and_round_trips_data(tmp_path: Path) -> None:
  path = tmp_path / "nested" / "data.json"
  data = {"nombre": "México", "estados": ["01", "32"]}

  written_path = FileStorage().write_json(path, data)

  assert written_path == path
  assert json.loads(path.read_text(encoding="utf-8")) == data
  assert "México" in path.read_text(encoding="utf-8")
