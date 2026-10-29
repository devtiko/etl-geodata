"""Punto de entrada y composición de dependencias del ETL."""

from etl.cli import create_parser
from etl.core.logging import configure_logging
from etl.extract.inegi_client import InegiClient
from etl.extract.inegi_persist import InegiPersist
from etl.extract.inegi_service import InegiService
from etl.load.geography_persist import GeographyPersist
from etl.pipelines.inegi_pipeline import InegiPipeline
from etl.shared.cache import RequestCache
from etl.shared.file_storage import FileStorage
from etl.transform.geography_merger import GeographyMerger


def main() -> None:
  """Descarga uno o todos los estados con sus municipios y localidades."""
  configure_logging()
  args = create_parser().parse_args()

  client = InegiClient()
  storage = FileStorage()
  cache = RequestCache(storage)

  try:
    service = InegiService(
      cache=cache,
      client=client,
      refresh=args.refresh,
      persist=InegiPersist(storage),
    )

    pipeline = InegiPipeline(
      service=service,
      merger=GeographyMerger(),
      persist=GeographyPersist(storage),
    )

    pipeline.run(state_code=args.state)
  finally:
    cache.save()
    client.close()
