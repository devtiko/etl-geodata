from pathlib import Path

import pytest

from etl.shared.cache import RequestCache
from etl.shared.file_storage import FileStorage


def test_cache_get_returns_none_for_unknown_or_unusable_entries(tmp_path: Path) -> None:
  manifest = tmp_path / "requests.json"
  manifest.write_text(
    '{"missing-path": {}, "without-path": {"url": "https://example.test"}}',
    encoding="utf-8",
  )
  cache = RequestCache(FileStorage(), manifest)

  assert cache.get("unknown") is None
  assert cache.get("missing-path") is None
  assert cache.get("without-path") is None


def test_cache_reads_saved_response_and_persists_updates(tmp_path: Path) -> None:
  storage = FileStorage()
  manifest = tmp_path / "requests.json"
  response_path = storage.write_json(tmp_path / "responses" / "states.json", {"datos": []})
  cache = RequestCache(storage, manifest)

  cache.set(key="states", url="https://example.test/states", file_path=response_path)
  cache.save()

  reloaded = RequestCache(storage, manifest)
  assert reloaded.get("states") == {"datos": []}
  record = storage.read_json(manifest)
  assert isinstance(record, dict)
  assert record["states"]["url"] == "https://example.test/states"
  assert record["states"]["file_path"] == str(response_path)
  assert isinstance(record["states"]["saved_at"], str)


def test_cache_set_ignores_responses_that_were_not_persisted(tmp_path: Path) -> None:
  manifest = tmp_path / "requests.json"
  cache = RequestCache(FileStorage(), manifest)

  cache.set(key="states", url="https://example.test/states", file_path=None)
  cache.save()

  assert FileStorage().read_json(manifest) == {}


def test_cache_rejects_non_object_manifest(tmp_path: Path) -> None:
  manifest = tmp_path / "requests.json"
  manifest.write_text("[]", encoding="utf-8")

  with pytest.raises(TypeError, match="debe contener un objeto JSON"):
    RequestCache(FileStorage(), manifest)
