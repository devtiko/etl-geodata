import pytest
from httpx import HTTPStatusError, MockTransport, Request, Response

from etl.extract.inegi_client import InegiClient


def test_client_raises_for_http_error_responses() -> None:
  def respond(request: Request) -> Response:
    return Response(503, json={"error": "unavailable"}, request=request)

  client = InegiClient(transport=MockTransport(respond))
  try:
    with pytest.raises(HTTPStatusError, match="503"):
      client.get_state("01")
  finally:
    client.close()
