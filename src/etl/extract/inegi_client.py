"""Cliente HTTP para el Servicio Web del Catálogo Único de INEGI."""

from httpx import BaseTransport, Client, Response

from etl.core.config import Settings
from etl.shared.http import DelayedTransport, raise_for_status


class InegiClient:
  """Realiza solicitudes HTTP a la API del Catálogo Único de INEGI."""

  def __init__(self, transport: BaseTransport | None = None) -> None:
    self._client: Client = Client(
      timeout=30.0,
      transport=transport if transport is not None else DelayedTransport(0.2),
      base_url=Settings.INEGI_API_BASE_URL.rstrip("/") + "/",
      event_hooks={"response": [raise_for_status]},
    )

  def get_states(self) -> Response:
    """Obtiene el catálogo de estados."""
    return self._client.get("mgee")

  def get_state(self, state_code: str) -> Response:
    """Obtiene los datos de un estado por su clave."""
    return self._client.get(f"mgee/{state_code}")

  def get_municipalities(self, state_code: str) -> Response:
    """Obtiene los municipios de un estado."""
    return self._client.get(f"mgem/{state_code}")

  def get_localities(self, state_code: str, municipality_code: str) -> Response:
    """Obtiene las localidades de un municipio."""
    return self._client.get(f"localidades/{state_code}/{municipality_code}")

  def get_state_geometries(self) -> Response:
    """Obtiene las geometrías de todos los estados."""
    return self._client.get("geo/mgee")

  def get_state_geometry(self, state_code: str) -> Response:
    """Obtiene la geometría de un estado por su clave."""
    return self._client.get(f"geo/mgee/{state_code}")

  def get_municipality_geometries(self, state_code: str) -> Response:
    """Obtiene las geometrías municipales de un estado."""
    return self._client.get(f"geo/mgem/{state_code}")

  def get_locality_geometries(
    self, state_code: str, municipality_code: str | None = None
  ) -> Response:
    """Obtiene polígonos de localidades de un estado o municipio."""
    endpoint = f"geo/localidades/pol/{state_code}"
    if municipality_code is not None:
      endpoint = f"{endpoint}/{municipality_code}"
    return self._client.get(endpoint)

  def close(self) -> None:
    """Cierra el cliente HTTP y libera sus conexiones."""
    self._client.close()
