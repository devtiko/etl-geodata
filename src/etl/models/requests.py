"""Tipos para los metadatos de solicitudes guardados en caché."""

from typing import TypedDict


class RequestRecord(TypedDict):
  """Metadatos de una solicitud guardada en el manifiesto."""

  url: str
  file_path: str
  saved_at: str
