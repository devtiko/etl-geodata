"""Configuración general de la aplicación."""

from pathlib import Path


class Settings:
  """Opciones de ejecución compartidas por los componentes del ETL."""

  LOG_LEVEL: str = "INFO"
  DATA_DIR: Path = Path("data")
  INEGI_API_BASE_URL: str = "https://gaia.inegi.org.mx/wscatgeo/v2"
