"""Modelos de salida para datos geográficos combinados."""

from typing import Literal

from pydantic import BaseModel

from etl.models.geography import MultiPolygonCoordinates


class MergedGeometry(BaseModel):
  """Geometría reducida para la salida del merge."""

  type: Literal["MultiPolygon"]
  crs: str | None = None
  coordinates: MultiPolygonCoordinates


class MergedState(BaseModel):
  """Campos de estado conservados en la salida procesada."""

  cvegeo: str
  cve_ent: str
  nomgeo: str | None = None
  nom_abrev: str | None = None
  geometry: MergedGeometry | None = None


class MergedMunicipality(BaseModel):
  """Campos de municipio conservados en la salida procesada."""

  cvegeo: str
  cve_ent: str
  cve_mun: str
  nomgeo: str | None = None
  geometry: MergedGeometry | None = None


class MergedLocality(BaseModel):
  """Campos de localidad conservados en la salida procesada."""

  cvegeo: str
  cve_ent: str
  cve_mun: str
  cve_loc: str | None = None
  nomgeo: str | None = None
  latitud: str | None = None
  longitud: str | None = None
  geometry: MergedGeometry | None = None
