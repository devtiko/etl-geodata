"""Lectura y escritura genérica de archivos JSON."""

import json
from pathlib import Path


class FileStorage:
  """Lee y escribe datos JSON en las rutas indicadas."""

  def _to_path(self, path: str | Path) -> Path:
    """Devuelve la ruta como ``Path``, sin reconstruirla si ya lo es."""
    return path if isinstance(path, Path) else Path(path)

  def read_json(self, path: str | Path, *, default: object = None) -> object:
    """Lee JSON, devuelve ``default`` si falta o None si no se puede decodificar."""
    file_path = self._to_path(path)
    try:
      return json.loads(file_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
      return default
    except json.JSONDecodeError:
      return None

  def write_json(self, path: str | Path, data: object) -> Path:
    """Crea los directorios necesarios y escribe datos como JSON."""
    file_path = self._to_path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
      json.dumps(data, ensure_ascii=False, indent=2),
      encoding="utf-8",
    )
    return file_path
