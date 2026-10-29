"""Persistencia de respuestas crudas del servicio de INEGI."""

from __future__ import annotations

from pathlib import Path

from etl.core.config import Settings
from etl.shared.file_storage import FileStorage


class InegiPersist:
  """Escribe las respuestas crudas de INEGI en el directorio de datos raw."""

  def __init__(self, storage: FileStorage) -> None:
    self._storage: FileStorage = storage
    self._raw_dir: Path = Settings.DATA_DIR / "raw"
    self._states_dir: Path = self._raw_dir / "states"
    self._municipalities_dir: Path = self._raw_dir / "municipalities"
    self._localities_dir: Path = self._raw_dir / "localities"

  def save_states(self, data: object) -> Path:
    """Persiste el catálogo de estados."""
    return self._storage.write_json(self._states_dir / "all.json", data)

  def save_state(self, data: object, state_code: str) -> Path:
    """Persiste la respuesta de un estado específico."""
    return self._storage.write_json(self._states_dir / f"{state_code}.json", data)

  def save_municipalities(self, data: object, state_code: str) -> Path:
    """Persiste el catálogo de municipios de un estado."""
    return self._storage.write_json(
      self._municipalities_dir / f"{state_code}.json", data
    )

  def save_localities(
    self, data: object, state_code: str, municipality_code: str
  ) -> Path:
    """Persiste el catálogo de localidades de un municipio."""
    return self._storage.write_json(
      self._localities_dir / f"{state_code}_{municipality_code}.json",
      data,
    )

  def save_state_geometries(self, data: object) -> Path:
    """Persiste las geometrías de todos los estados."""
    return self._storage.write_json(self._raw_dir / "states.geojson", data)

  def save_state_geometry(self, data: object, state_code: str) -> Path:
    """Persiste la geometría de un estado específico."""
    return self._storage.write_json(self._states_dir / f"{state_code}.geojson", data)

  def save_municipality_geometries(self, data: object, state_code: str) -> Path:
    """Persiste las geometrías municipales de un estado."""
    return self._storage.write_json(
      self._municipalities_dir / f"{state_code}.geojson", data
    )

  def save_locality_geometries(
    self, data: object, state_code: str, municipality_code: str
  ) -> Path:
    """Persiste las geometrías de localidades de un municipio."""
    return self._storage.write_json(
      self._localities_dir / f"{state_code}_{municipality_code}.geojson",
      data,
    )
