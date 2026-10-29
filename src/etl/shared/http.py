"""Utilidades HTTP compartidas basadas en HTTPX."""

import time
from typing import override

from httpx import BaseTransport, HTTPTransport, Request, Response


class DelayedTransport(BaseTransport):
  """Espacia las solicitudes enviadas por un transporte HTTPX."""

  def __init__(self, delay: float) -> None:
    if delay < 0:
      raise ValueError("delay no puede ser negativo")

    self._delay: float = delay
    self._transport: HTTPTransport = HTTPTransport()

  @override
  def handle_request(self, request: Request) -> Response:
    if self._delay > 0:
      time.sleep(self._delay)
    return self._transport.handle_request(request)

  @override
  def close(self) -> None:
    self._transport.close()


def raise_for_status(response: Response) -> None:
  """Lanza una excepción HTTPX si la respuesta tiene un estado de error."""
  response.raise_for_status()
