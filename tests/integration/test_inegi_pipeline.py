import json
from pathlib import Path

from httpx import MockTransport, Request, Response
from pytest import MonkeyPatch

from etl.core.config import Settings
from etl.extract.inegi_client import InegiClient
from etl.extract.inegi_persist import InegiPersist
from etl.extract.inegi_service import InegiService
from etl.load.geography_persist import GeographyPersist
from etl.pipelines.inegi_pipeline import InegiPipeline
from etl.shared.cache import RequestCache
from etl.shared.file_storage import FileStorage
from etl.transform.geography_merger import GeographyMerger


def test_pipeline_processes_state_from_http_responses_to_processed_files(
  tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
  monkeypatch.setattr(Settings, "DATA_DIR", tmp_path / "data")
  geometry = {
    "type": "MultiPolygon",
    "coordinates": [[[[1, 2], [3, 4], [5, 6]]]],
    "crs": {"properties": {"name": "EPSG:4326"}},
  }
  responses = {
    "/mgee/01": {
      "datos": {"cvegeo": "01", "cve_ent": "01", "nomgeo": "Estado de prueba"}
    },
    "/geo/mgee/01": {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {"cvegeo": "01", "cve_ent": "01"},
          "geometry": geometry,
        }
      ],
    },
    "/mgem/01": {
      "datos": [
        {"cvegeo": "01001", "cve_ent": "01", "cve_mun": "001", "nomgeo": "Municipio de prueba"}
      ],
      "numReg": 1,
    },
    "/geo/mgem/01": {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {"cvegeo": "01001", "cve_ent": "01", "cve_mun": "001"},
          "geometry": geometry,
        }
      ],
    },
    "/localidades/01/001": {
      "datos": [
        {
          "cvegeo": "010010001",
          "cve_ent": "01",
          "cve_mun": "001",
          "cve_loc": "0001",
          "nomgeo": "Localidad de prueba",
        }
      ],
      "numReg": 1,
    },
    "/geo/localidades/pol/01/001": {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {
            "cvegeo": "010010001",
            "cve_ent": "01",
            "cve_mun": "001",
            "latitud": "19.0",
            "longitud": "-99.0",
          },
          "geometry": geometry,
        }
      ],
    },
  }
  requested_paths: list[str] = []

  def respond(request: Request) -> Response:
    path = request.url.path.removeprefix("/wscatgeo/v2")
    requested_paths.append(path)
    return Response(200, json=responses[path], request=request)

  storage = FileStorage()
  cache = RequestCache(storage, tmp_path / "data" / "requests.json")
  client = InegiClient(transport=MockTransport(respond))
  service = InegiService(
    client=client,
    persist=InegiPersist(storage),
    cache=cache,
  )
  pipeline = InegiPipeline(
    service=service,
    merger=GeographyMerger(),
    persist=GeographyPersist(storage),
  )

  try:
    pipeline.run(state_code="01")
    cache.save()
    assert service.get_state("01").datos.nomgeo == "Estado de prueba"
  finally:
    client.close()

  assert requested_paths == list(responses)

  states = json.loads((tmp_path / "data/processed/states.json").read_text())
  municipalities = json.loads(
    (tmp_path / "data/processed/municipalities/01.json").read_text()
  )
  localities = json.loads(
    (tmp_path / "data/processed/localities/01_001.json").read_text()
  )
  raw_response = json.loads((tmp_path / "data/raw/states/01.json").read_text())

  assert states[0]["cvegeo"] == "01"
  assert states[0]["geometry"]["crs"] == "4326"
  assert municipalities[0]["cvegeo"] == "01001"
  assert localities[0]["cvegeo"] == "010010001"
  assert localities[0]["latitud"] == "19.0"
  assert localities[0]["longitud"] == "-99.0"
  assert raw_response["datos"]["nomgeo"] == "Estado de prueba"
  assert (tmp_path / "data/requests.json").is_file()
