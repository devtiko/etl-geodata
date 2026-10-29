from pathlib import Path

import pytest
from httpx import MockTransport, Request, Response
from pydantic import ValidationError
from pytest import MonkeyPatch

from etl.core.config import Settings
from etl.extract.inegi_client import InegiClient
from etl.extract.inegi_persist import InegiPersist
from etl.extract.inegi_service import InegiService
from etl.shared.cache import RequestCache
from etl.shared.file_storage import FileStorage


def _state_response() -> dict[str, object]:
  return {
    "datos": {"cvegeo": "01", "cve_ent": "01", "nomgeo": "Estado de prueba"},
    "numReg": 1,
  }


def test_service_reuses_persisted_cache_on_a_new_instance(
  tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
  monkeypatch.setattr(Settings, "DATA_DIR", tmp_path / "data")
  storage = FileStorage()
  manifest_path = tmp_path / "data" / "requests.json"
  requested_paths: list[str] = []

  def respond(request: Request) -> Response:
    requested_paths.append(request.url.path)
    return Response(200, json=_state_response(), request=request)

  cache = RequestCache(storage, manifest_path)
  client = InegiClient(transport=MockTransport(respond))
  service = InegiService(
    client=client,
    persist=InegiPersist(storage),
    cache=cache,
  )
  try:
    assert service.get_state("01").datos.nomgeo == "Estado de prueba"
    cache.save()
  finally:
    client.close()

  def unexpected_request(request: Request) -> Response:
    pytest.fail(f"No se esperaba una solicitud HTTP: {request.url}")

  cached_client = InegiClient(transport=MockTransport(unexpected_request))
  cached_service = InegiService(
    client=cached_client,
    persist=InegiPersist(storage),
    cache=RequestCache(storage, manifest_path),
  )
  try:
    assert cached_service.get_state("01").datos.nomgeo == "Estado de prueba"
  finally:
    cached_client.close()

  assert len(requested_paths) == 1


def test_service_rejects_invalid_http_payload_without_caching_it(
  tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
  monkeypatch.setattr(Settings, "DATA_DIR", tmp_path / "data")
  storage = FileStorage()
  manifest_path = tmp_path / "data" / "requests.json"

  def respond(request: Request) -> Response:
    return Response(200, json={"unexpected": True}, request=request)

  client = InegiClient(transport=MockTransport(respond))
  cache = RequestCache(storage, manifest_path)
  service = InegiService(
    client=client,
    persist=InegiPersist(storage),
    cache=cache,
  )
  try:
    with pytest.raises(ValidationError):
      service.get_state("01")
    cache.save()
  finally:
    client.close()

  assert not (tmp_path / "data/raw/states/01.json").exists()
  assert storage.read_json(manifest_path) == {}
