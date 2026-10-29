"""Caché de respuestas HTTP registradas en un manifiesto JSON."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from etl.core.config import Settings
from etl.models.requests import RequestRecord
from etl.shared.file_storage import FileStorage


class RequestCache:
  """Resuelve respuestas previamente guardadas a partir de su endpoint."""

  def __init__(
    self,
    storage: FileStorage,
    manifest_path: Path | None = None,
  ) -> None:
    self._storage: FileStorage = storage
    self._manifest_path: Path = manifest_path or Settings.DATA_DIR / "requests.json"
    self._requests: dict[str, RequestRecord] = self._get_all()

  def _get_all(self) -> dict[str, RequestRecord]:
    """Carga el manifiesto existente o devuelve un diccionario vacío."""
    existing = self._storage.read_json(self._manifest_path, default={})
    if not isinstance(existing, dict):
      raise TypeError(f"{self._manifest_path} debe contener un objeto JSON")
    return cast(dict[str, RequestRecord], existing)

  def get(self, endpoint: str) -> object | None:
    """Lee los datos crudos asociados a un endpoint, si están en caché."""
    record = self._requests.get(endpoint)
    if not isinstance(record, dict):
      return None

    file_path = record.get("file_path")
    if not file_path:
      return None
    return self._storage.read_json(file_path)

  def set(
    self,
    *,
    key: str,
    url: str,
    file_path: Path | None,
  ) -> None:
    """Registra una respuesta después de que se haya persistido en disco."""
    if file_path is None:
      return

    self._requests[key] = {
      "url": url,
      "file_path": str(file_path),
      "saved_at": datetime.now(UTC).isoformat(),
    }

  def save(self) -> None:
    """Persiste el manifiesto de solicitudes actualizado."""
    self._storage.write_json(self._manifest_path, self._requests)
