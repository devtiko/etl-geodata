"""Validadores de argumentos de ejecución."""

import argparse


def normalize_state_code(value: str) -> str:
  """Valida que la clave esté entre 1 y 32 y la normaliza a dos dígitos."""
  if not value.isascii() or not value.isdecimal() or len(value) > 2:
    raise argparse.ArgumentTypeError(
      "la clave del estado debe ser un número entre 1 y 32"
    )
  state_number = int(value)
  if not 1 <= state_number <= 32:
    raise argparse.ArgumentTypeError(
      "la clave del estado debe estar en el rango de 1 a 32"
    )
  return str(state_number).zfill(2)
