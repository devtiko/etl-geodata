"""Persistencia de los registros geográficos transformados."""

from pathlib import Path
from typing import cast

from etl.core.config import Settings
from etl.models.merged import MergedLocality, MergedMunicipality, MergedState
from etl.shared.file_storage import FileStorage


class GeographyPersist:
  """Guarda los registros geográficos procesados como archivos JSON."""

  def __init__(self, storage: FileStorage) -> None:
    self._storage: FileStorage = storage
    self._processed_dir: Path = Settings.DATA_DIR / "processed"
    self._states_file: Path = self._processed_dir / "states.json"
    self._municipalities_dir: Path = self._processed_dir / "municipalities"
    self._localities_dir: Path = self._processed_dir / "localities"

  def save_states(self, states: list[MergedState]) -> Path:
    """Guarda todos los estados transformados en un archivo JSON."""
    records = [state.model_dump(mode="json") for state in states]
    return self._storage.write_json(self._states_file, records)

  def save_state(self, state: MergedState) -> Path:
    """Agrega o actualiza un estado del archivo usando su clave cvegeo."""
    states = self._storage.read_json(self._states_file, default=[])
    if not isinstance(states, list):
      raise TypeError("data/processed/states.json debe contener una lista JSON")
    states = cast(list[object], states)

    state_data = state.model_dump(mode="json")
    for index, existing_state in enumerate(states):
      if (
        isinstance(existing_state, dict)
        and cast(dict[str, object], existing_state).get("cvegeo") == state.cvegeo
      ):
        states[index] = state_data
        break
    else:
      states.append(state_data)

    return self._storage.write_json(self._states_file, states)

  def save_municipalities(
    self,
    municipalities_by_state: dict[str, list[MergedMunicipality]],
  ) -> dict[str, Path]:
    """Guarda un archivo de municipios transformados por estado."""
    saved_files: dict[str, Path] = {}
    for state_code, municipalities in municipalities_by_state.items():
      records = [
        municipality.model_dump(mode="json") for municipality in municipalities
      ]
      path = self._municipalities_dir / f"{state_code}.json"
      saved_files[state_code] = self._storage.write_json(path, records)
    return saved_files

  def save_localities(
    self,
    localities_by_municipality: dict[str, list[MergedLocality]],
  ) -> dict[str, Path]:
    """Guarda un archivo de localidades transformadas por municipio."""
    saved_files: dict[str, Path] = {}
    for municipality_code, localities in localities_by_municipality.items():
      records = [locality.model_dump(mode="json") for locality in localities]
      path = self._localities_dir / f"{municipality_code}.json"
      saved_files[municipality_code] = self._storage.write_json(path, records)
    return saved_files
