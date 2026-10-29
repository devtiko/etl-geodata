import pytest

from etl.models.geography import (
  LocalityCatalogResponse,
  LocalityGeoJSONResponse,
  MunicipalityCatalogResponse,
  MunicipalityGeoJSONResponse,
  StateCatalogResponse,
  StateGeoJSONResponse,
)
from etl.transform.geography_merger import GeographyMerger


def test_merge_states_matches_features_and_extracts_crs() -> None:
  catalog = StateCatalogResponse.model_validate(
    {
      "datos": [
        {"cvegeo": "01", "cve_ent": "01", "nomgeo": "Aguascalientes"},
        {"cvegeo": "02", "cve_ent": "02", "nomgeo": "Baja California"},
      ],
      "numReg": 2,
    }
  )
  geojson = StateGeoJSONResponse.model_validate(
    {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {"cvegeo": "01", "cve_ent": "01"},
          "geometry": {
            "type": "MultiPolygon",
            "coordinates": [[[[1, 2], [3, 4], [5, 6]]]],
            "crs": {"properties": {"name": "EPSG:4326"}},
          },
        }
      ],
    }
  )

  merged = GeographyMerger().merge_states(catalog, geojson)

  assert len(merged) == 2
  assert merged[0].geometry is not None
  assert merged[0].geometry.crs == "4326"
  assert merged[0].geometry.coordinates == [[[(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)]]]
  assert merged[1].geometry is None


def test_merge_municipalities_groups_records_by_state() -> None:
  catalog = MunicipalityCatalogResponse.model_validate(
    {
      "datos": [
        {"cvegeo": "01001", "cve_ent": "01", "cve_mun": "001"},
        {"cvegeo": "01002", "cve_ent": "01", "cve_mun": "002"},
        {"cvegeo": "02001", "cve_ent": "02", "cve_mun": "001"},
      ],
      "numReg": 3,
    }
  )
  geojson = MunicipalityGeoJSONResponse.model_validate(
    {"type": "FeatureCollection", "features": []}
  )

  merged = GeographyMerger().merge_municipalities(catalog, geojson)

  assert {state: [municipality.cvegeo for municipality in values] for state, values in merged.items()} == {
    "01": ["01001", "01002"],
    "02": ["02001"],
  }


def test_merge_localities_completes_missing_coordinates_and_groups_by_municipality() -> None:
  catalog = LocalityCatalogResponse.model_validate(
    {
      "datos": [
        {
          "cvegeo": "010010001",
          "cve_ent": "01",
          "cve_mun": "001",
          "cve_loc": "0001",
          "latitud": "19.0",
        }
      ],
      "numReg": 1,
    }
  )
  geojson = LocalityGeoJSONResponse.model_validate(
    {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {
            "cvegeo": "010010001",
            "cve_ent": "01",
            "cve_mun": "001",
            "latitud": "20.0",
            "longitud": "-99.0",
          },
        }
      ],
    }
  )

  merged = GeographyMerger().merge_localities(catalog, geojson)

  locality = merged["01_001"][0]
  assert locality.latitud == "19.0"
  assert locality.longitud == "-99.0"


def test_merge_raises_when_catalog_record_has_no_geographic_code() -> None:
  catalog = StateCatalogResponse.model_validate(
    {"datos": [{"cve_ent": "01"}], "numReg": 1}
  )
  geojson = StateGeoJSONResponse.model_validate(
    {"type": "FeatureCollection", "features": []}
  )

  with pytest.raises(ValueError, match="debe incluir cvegeo"):
    GeographyMerger().merge_states(catalog, geojson)
