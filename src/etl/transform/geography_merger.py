"""Combina modelos de catálogos de INEGI con sus geometrías GeoJSON."""

from collections.abc import Callable, Sequence

from etl.models.geography import (
  LocalityCatalogResponse,
  LocalityGeoJSONFeature,
  LocalityGeoJSONResponse,
  LocalityJSONRecord,
  MultiPolygonGeometry,
  MunicipalityCatalogResponse,
  MunicipalityGeoJSONResponse,
  StateCatalogResponse,
  StateGeoJSONResponse,
  StateResponse,
)
from etl.models.merged import (
  MergedGeometry,
  MergedLocality,
  MergedMunicipality,
  MergedState,
)


class GeographyMerger:
  """Combina registros tipados de INEGI con sus geometrías."""

  def _require_cvegeo(self, cvegeo: str | None) -> str:
    """Devuelve la clave geográfica o falla si falta en el registro fuente."""
    if cvegeo is None:
      raise ValueError("el registro geográfico debe incluir cvegeo")
    return cvegeo

  def _build_features_by_code[FeatureT](
    self,
    features: Sequence[FeatureT],
    get_code: Callable[[FeatureT], str | None],
  ) -> dict[str, FeatureT]:
    """Indexa features por su clave geográfica."""
    features_by_code: dict[str, FeatureT] = {}
    for feature in features:
      code = get_code(feature)
      if code is not None:
        features_by_code[code] = feature
    return features_by_code

  def _extract_crs_code(self, geometry: MultiPolygonGeometry) -> str | None:
    """Obtiene el SRID de la referencia espacial de la geometría."""

    if geometry.crs is None:
      return None

    properties = geometry.crs.get("properties")
    if not isinstance(properties, dict):
      return None
    name = properties.get("name")
    if not isinstance(name, str):
      return None
    parts = name.split(":")
    return parts[1] if len(parts) > 1 else None

  def _locality_coordinates(
    self,
    record: LocalityJSONRecord,
    feature: LocalityGeoJSONFeature | None,
  ) -> tuple[str | None, str | None]:
    """Conserva las coordenadas del catálogo y completa las que falten."""
    latitud = record.latitud
    longitud = record.longitud
    if feature is not None:
      if latitud is None:
        latitud = feature.properties.latitud
      if longitud is None:
        longitud = feature.properties.longitud
    return latitud, longitud

  def merge_states(
    self,
    catalog: StateCatalogResponse,
    geojson: StateGeoJSONResponse,
  ) -> list[MergedState]:
    """Combina varios estados con sus geometrías."""
    features_by_code = self._build_features_by_code(
      geojson.features,
      lambda feature: feature.properties.cvegeo,
    )

    merged_records: list[MergedState] = []

    for record in catalog.datos:
      feature = None
      if record.cvegeo is not None:
        feature = features_by_code.get(record.cvegeo)

      geometry = None
      if feature is not None and feature.geometry is not None:
        geometry = MergedGeometry(
          type=feature.geometry.type,
          crs=self._extract_crs_code(feature.geometry),
          coordinates=feature.geometry.coordinates,
        )

      merged = MergedState(
        cvegeo=self._require_cvegeo(record.cvegeo),
        cve_ent=record.cve_ent,
        nomgeo=record.nomgeo,
        nom_abrev=record.nom_abrev,
        geometry=geometry,
      )

      merged_records.append(merged)

    return merged_records

  def merge_state(
    self,
    state: StateResponse,
    geojson: StateGeoJSONResponse,
  ) -> MergedState:
    """Combina un estado individual con su geometría."""

    features_by_code = self._build_features_by_code(
      geojson.features,
      lambda feature: feature.properties.cvegeo,
    )

    feature = None
    if state.datos.cvegeo is not None:
      feature = features_by_code.get(state.datos.cvegeo)

    geometry = None
    if feature is not None and feature.geometry is not None:
      geometry = MergedGeometry(
        type=feature.geometry.type,
        crs=self._extract_crs_code(feature.geometry),
        coordinates=feature.geometry.coordinates,
      )

    return MergedState(
      cvegeo=self._require_cvegeo(state.datos.cvegeo),
      cve_ent=state.datos.cve_ent,
      nomgeo=state.datos.nomgeo,
      nom_abrev=state.datos.nom_abrev,
      geometry=geometry,
    )

  def merge_municipalities(
    self,
    catalog: MunicipalityCatalogResponse,
    geojson: MunicipalityGeoJSONResponse,
  ) -> dict[str, list[MergedMunicipality]]:
    """Combina municipios con sus geometrías."""
    features_by_code = self._build_features_by_code(
      geojson.features,
      lambda feature: feature.properties.cvegeo,
    )

    municipalities_by_state: dict[str, list[MergedMunicipality]] = {}

    for record in catalog.datos:
      feature = None
      if record.cvegeo is not None:
        feature = features_by_code.get(record.cvegeo)

      geometry = None
      if feature is not None and feature.geometry is not None:
        geometry = MergedGeometry(
          type=feature.geometry.type,
          crs=self._extract_crs_code(feature.geometry),
          coordinates=feature.geometry.coordinates,
        )

      merged = MergedMunicipality(
        cvegeo=self._require_cvegeo(record.cvegeo),
        cve_ent=record.cve_ent,
        cve_mun=record.cve_mun,
        nomgeo=record.nomgeo,
        geometry=geometry,
      )

      municipalities_by_state.setdefault(record.cve_ent, []).append(merged)

    return municipalities_by_state

  def merge_localities(
    self,
    catalog: LocalityCatalogResponse,
    geojson: LocalityGeoJSONResponse,
  ) -> dict[str, list[MergedLocality]]:
    """Combina localidades y completa latitud/longitud cuando falten."""
    features_by_code = self._build_features_by_code(
      geojson.features,
      lambda feature: feature.properties.cvegeo,
    )

    localities_by_municipality: dict[str, list[MergedLocality]] = {}

    for record in catalog.datos:
      feature = None
      if record.cvegeo is not None:
        feature = features_by_code.get(record.cvegeo)

      latitud, longitud = self._locality_coordinates(record, feature)

      geometry = None
      if feature is not None and feature.geometry is not None:
        geometry = MergedGeometry(
          type=feature.geometry.type,
          crs=self._extract_crs_code(feature.geometry),
          coordinates=feature.geometry.coordinates,
        )

      merged = MergedLocality(
        cvegeo=self._require_cvegeo(record.cvegeo),
        cve_ent=record.cve_ent,
        cve_mun=record.cve_mun,
        cve_loc=record.cve_loc,
        nomgeo=record.nomgeo,
        latitud=latitud,
        longitud=longitud,
        geometry=geometry,
      )

      group_key = f"{record.cve_ent}_{record.cve_mun}"
      localities_by_municipality.setdefault(group_key, []).append(merged)

    return localities_by_municipality
