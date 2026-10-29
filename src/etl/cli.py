"""Configuración de la interfaz de línea de comandos."""

import argparse

from etl.shared.validators import normalize_state_code


def create_parser() -> argparse.ArgumentParser:
  """Construye el parser de argumentos del ETL."""
  parser = argparse.ArgumentParser(description="ETL geográfico de INEGI")
  parser.add_argument(
    "--state",
    type=normalize_state_code,
    help=(
      "Clave del estado entre 1 y 32 (por ejemplo, 1 o 01); si se omite, consulta todos"
    ),
  )
  parser.add_argument(
    "--refresh",
    action="store_true",
    help="Forzar la actualización e ignorar la caché (por defecto, se reutiliza)",
  )
  return parser
