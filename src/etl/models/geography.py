"""Modelos tipados para las respuestas geográficas de INEGI."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

type JsonValue = (
  dict[str, JsonValue] | list[JsonValue] | str | int | float | bool | None
)
type Position = tuple[float, float] | tuple[float, float, float]
type MultiPolygonCoordinates = list[list[list[Position]]]


class StateJSONRecord(BaseModel):
  """Registro tabular de un estado."""

  cvegeo: str | None = None
  cve_ent: str
  nomgeo: str | None = None
  nom_abrev: str | None = None
  pob_total: str | None = None
  pob_femenina: str | None = None
  pob_masculina: str | None = None
  total_viviendas_habitadas: str | None = None


class MunicipalityJSONRecord(BaseModel):
  """Registro tabular de municipio."""

  cvegeo: str | None = None
  cve_ent: str
  cve_mun: str
  nomgeo: str | None = None
  cve_cab: str | None = None
  pob_total: str | None = None
  pob_femenina: str | None = None
  pob_masculina: str | None = None
  total_viviendas_habitadas: str | None = None


class LocalityJSONRecord(BaseModel):
  """Registro tabular de localidad."""

  cvegeo: str | None = None
  cve_ent: str
  cve_mun: str
  cve_loc: str | None = None
  nomgeo: str | None = None
  ambito: str | None = None
  latitud: str | None = None
  longitud: str | None = None
  altitud: str | None = None
  pob_total: str | None = None
  total_viviendas_habitadas: str | None = None
  cve_carta: str | None = None
  estatus: int | None = None
  periodo: str | None = None


class CatalogResponse[RecordT: BaseModel](BaseModel):
  """Envoltura de los catálogos tabulares de INEGI."""

  datos: list[RecordT]
  metadatos: dict[str, str] | None = None
  numReg: int


class StateCatalogResponse(CatalogResponse[StateJSONRecord]):
  """Respuesta del catálogo de estados."""


class StateResponse(BaseModel):
  """Respuesta de la consulta de un estado por clave."""

  datos: StateJSONRecord
  metadatos: dict[str, str] | None = None
  numReg: int | None = None


class MunicipalityCatalogResponse(CatalogResponse[MunicipalityJSONRecord]):
  """Respuesta del catálogo de municipios."""


class LocalityCatalogResponse(CatalogResponse[LocalityJSONRecord]):
  """Respuesta del catálogo de localidades."""


class StateGeoJSONProperties(BaseModel):
  """Propiedades observadas en los GeoJSON de estados."""

  cvegeo: str | None = None
  cve_ent: str
  nomgeo: str | None = None
  nom_abrev: str | None = None
  pob_total: str | None = None
  pob_femenina: str | None = None
  pob_masculina: str | None = None
  total_viviendas_habitadas: str | None = None


class MunicipalityGeoJSONProperties(BaseModel):
  """Propiedades observadas en los GeoJSON de municipios."""

  cvegeo: str | None = None
  cve_ent: str
  cve_mun: str
  nomgeo: str | None = None
  cve_cab: str | None = None
  pob_total: str | None = None
  pob_femenina: str | None = None
  pob_masculina: str | None = None
  total_viviendas_habitadas: str | None = None


class LocalityGeoJSONProperties(BaseModel):
  """Propiedades observadas en los GeoJSON de localidades."""

  cvegeo: str | None = None
  cve_ent: str
  cve_mun: str
  cve_loc: str | None = None
  nom_loc: str | None = None
  ambito: str | None = None
  latitud: str | None = None
  longitud: str | None = None
  altitud: str | None = None
  pob_total: str | None = None
  total_viviendas_habitadas: str | None = None
  cve_carta: str | None = None
  estatus: int | None = None
  periodo: str | None = None


class MultiPolygonGeometry(BaseModel):
  """Geometría multipolígono publicada en las capas consultadas de INEGI."""

  type: Literal["MultiPolygon"]
  coordinates: MultiPolygonCoordinates
  crs: dict[str, JsonValue] | None = None


class GeoJSONFeature[PropertiesT: BaseModel](BaseModel):
  """Feature GeoJSON parametrizado por el modelo de propiedades geográficas."""

  type: Literal["Feature"]
  properties: PropertiesT
  geometry: MultiPolygonGeometry | None = None
  numReg: int | None = None


class StateGeoJSONFeature(GeoJSONFeature[StateGeoJSONProperties]):
  """Feature GeoJSON de un estado."""


class MunicipalityGeoJSONFeature(GeoJSONFeature[MunicipalityGeoJSONProperties]):
  """Feature GeoJSON de un municipio."""


class LocalityGeoJSONFeature(GeoJSONFeature[LocalityGeoJSONProperties]):
  """Feature GeoJSON de una localidad."""


class GeoJSONFeatureCollection[FeatureT: BaseModel](BaseModel):
  """FeatureCollection GeoJSON parametrizada por su clase concreta de feature."""

  type: Literal["FeatureCollection"]
  features: list[FeatureT]
  metadatos: dict[str, str] | None = None
  totalReg: int | None = None


class StateGeoJSONResponse(GeoJSONFeatureCollection[StateGeoJSONFeature]):
  """Colección GeoJSON de estados."""


class MunicipalityGeoJSONResponse(GeoJSONFeatureCollection[MunicipalityGeoJSONFeature]):
  """Colección GeoJSON de municipios."""


class LocalityGeoJSONResponse(GeoJSONFeatureCollection[LocalityGeoJSONFeature]):
  """Colección GeoJSON de localidades."""
