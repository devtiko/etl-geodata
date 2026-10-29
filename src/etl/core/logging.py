"""Configuración del logging de la aplicación."""

import logging

from etl.core.config import Settings


def configure_logging(level: str | None = None) -> None:
    """Configura el logging raíz con un formato uniforme para el ETL."""
    configured_level = (level or Settings.LOG_LEVEL).upper()
    numeric_level = getattr(logging, configured_level, None)
    if not isinstance(numeric_level, int):
        raise TypeError(f"Nivel de logging no válido: {configured_level}")

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
