"""Obtención, validación, caché y persistencia de datos de INEGI."""

import logging
from typing import TypeVar

from httpx import Response
from pydantic import BaseModel, ValidationError

from etl.extract.inegi_client import InegiClient
from etl.extract.inegi_persist import InegiPersist
from etl.models.geography import (
  LocalityCatalogResponse,
  LocalityGeoJSONResponse,
  MunicipalityCatalogResponse,
  MunicipalityGeoJSONResponse,
  StateCatalogResponse,
  StateGeoJSONResponse,
  StateResponse,
)
from etl.shared.cache import RequestCache

logger = logging.getLogger(__name__)
TModel = TypeVar("TModel", bound=BaseModel)


class InegiService:
  """Devuelve modelos validados usando caché o consultando la API de INEGI."""

  def __init__(
    self,
    client: InegiClient,
    persist: InegiPersist,
    cache: RequestCache,
    refresh: bool = False,
  ) -> None:
    self._client: InegiClient = client
    self._persist: InegiPersist = persist
    self._cache: RequestCache = cache
    self._refresh: bool = refresh

  def _get_cached(self, request_key: str, model: type[TModel]) -> TModel | None:
    """Devuelve un modelo validado desde caché, si está disponible."""
    if self._refresh:
      return None

    cached_data = self._cache.get(request_key)
    if cached_data is None:
      return None

    try:
      data = model.model_validate(cached_data)
    except ValidationError:
      logger.warning(
        "Caché inválida para %s; se volverá a consultar",
        request_key,
        exc_info=True,
      )
      return None

    logger.info("Usando caché: %s", request_key)
    return data

  def _validate_response(
    self, response: Response, request_key: str, model: type[TModel]
  ) -> tuple[object, TModel]:
    """Decodifica y valida una respuesta HTTP, conservando los datos crudos."""
    try:
      raw_data = response.json()
      data = model.model_validate(raw_data)
    except (ValueError, ValidationError):
      logger.exception("Respuesta inválida para %s", request_key)
      raise

    return raw_data, data

  def get_states(self) -> StateCatalogResponse:
    """Obtiene el catálogo de estados."""

    request_key = "states"
    cached_data = self._get_cached(request_key, StateCatalogResponse)
    if cached_data is not None:
      return cached_data

    response = self._client.get_states()

    raw_data, data = self._validate_response(
      response, request_key, StateCatalogResponse
    )

    file_path = self._persist.save_states(raw_data)

    self._cache.set(
      key=request_key,
      url=str(response.url),
      file_path=file_path,
    )

    return data

  def get_state(self, state_code: str) -> StateResponse:
    """Obtiene los datos de un estado por su clave."""

    request_key = f"state_{state_code}"
    cached_data = self._get_cached(request_key, StateResponse)
    if cached_data is not None:
      return cached_data

    response = self._client.get_state(state_code)

    raw_data, data = self._validate_response(response, request_key, StateResponse)

    file_path = self._persist.save_state(raw_data, state_code)

    self._cache.set(
      key=request_key,
      url=str(response.url),
      file_path=file_path,
    )

    return data

  def get_municipalities(self, state_code: str) -> MunicipalityCatalogResponse:
    """Obtiene el catálogo de municipios de un estado."""
    request_key = f"municipalities_{state_code}"
    cached_data = self._get_cached(request_key, MunicipalityCatalogResponse)
    if cached_data is not None:
      return cached_data

    response = self._client.get_municipalities(state_code)

    raw_data, data = self._validate_response(
      response, request_key, MunicipalityCatalogResponse
    )

    file_path = self._persist.save_municipalities(raw_data, state_code)

    self._cache.set(
      key=request_key,
      url=str(response.url),
      file_path=file_path,
    )

    return data

  def get_localities(
    self, state_code: str, municipality_code: str
  ) -> LocalityCatalogResponse:
    """Obtiene las localidades de un municipio."""
    request_key = f"localities_{state_code}_{municipality_code}"
    cached_data = self._get_cached(request_key, LocalityCatalogResponse)
    if cached_data is not None:
      return cached_data

    response = self._client.get_localities(state_code, municipality_code)

    raw_data, data = self._validate_response(
      response, request_key, LocalityCatalogResponse
    )

    file_path = self._persist.save_localities(raw_data, state_code, municipality_code)

    self._cache.set(
      key=request_key,
      url=str(response.url),
      file_path=file_path,
    )

    return data

  def get_state_geometries(
    self,
  ) -> StateGeoJSONResponse:
    """Obtiene las geometrías de todos los estados."""
    request_key = "state_geometries"
    cached_data = self._get_cached(request_key, StateGeoJSONResponse)
    if cached_data is not None:
      return cached_data

    response = self._client.get_state_geometries()

    raw_data, data = self._validate_response(
      response, request_key, StateGeoJSONResponse
    )

    file_path = self._persist.save_state_geometries(raw_data)

    self._cache.set(
      key=request_key,
      url=str(response.url),
      file_path=file_path,
    )

    return data

  def get_state_geometry(self, state_code: str) -> StateGeoJSONResponse:
    """Obtiene la geometría de un estado por su clave."""
    request_key = f"state_geometry_{state_code}"
    cached_data = self._get_cached(request_key, StateGeoJSONResponse)
    if cached_data is not None:
      return cached_data

    response = self._client.get_state_geometry(state_code)

    raw_data, data = self._validate_response(
      response, request_key, StateGeoJSONResponse
    )

    file_path = self._persist.save_state_geometry(raw_data, state_code)

    self._cache.set(
      key=request_key,
      url=str(response.url),
      file_path=file_path,
    )

    return data

  def get_municipality_geometries(self, state_code: str) -> MunicipalityGeoJSONResponse:
    """Obtiene las geometrías municipales de un estado."""
    request_key = f"municipality_geometries_{state_code}"
    cached_data = self._get_cached(request_key, MunicipalityGeoJSONResponse)
    if cached_data is not None:
      return cached_data

    response = self._client.get_municipality_geometries(state_code)

    raw_data, data = self._validate_response(
      response, request_key, MunicipalityGeoJSONResponse
    )

    file_path = self._persist.save_municipality_geometries(raw_data, state_code)

    self._cache.set(
      key=request_key,
      url=str(response.url),
      file_path=file_path,
    )

    return data

  def get_locality_geometries(
    self, state_code: str, municipality_code: str
  ) -> LocalityGeoJSONResponse:
    """Obtiene polígonos de localidades de un municipio."""
    request_key = f"locality_geometries_{state_code}_{municipality_code}"
    cached_data = self._get_cached(request_key, LocalityGeoJSONResponse)
    if cached_data is not None:
      return cached_data

    response = self._client.get_locality_geometries(state_code, municipality_code)

    raw_data, data = self._validate_response(
      response, request_key, LocalityGeoJSONResponse
    )

    file_path = self._persist.save_locality_geometries(
      raw_data, state_code, municipality_code
    )

    self._cache.set(
      key=request_key,
      url=str(response.url),
      file_path=file_path,
    )

    return data
