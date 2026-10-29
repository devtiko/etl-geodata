"""Orquestación del flujo ETL de datos geográficos de INEGI."""

from etl.extract.inegi_service import InegiService
from etl.load.geography_persist import GeographyPersist
from etl.transform.geography_merger import GeographyMerger


class InegiPipeline:
  """Coordina extracción, transformación y persistencia de datos geográficos."""

  def __init__(
    self,
    service: InegiService,
    merger: GeographyMerger,
    persist: GeographyPersist,
  ) -> None:
    self._merger: GeographyMerger = merger
    self._service: InegiService = service
    self._persist: GeographyPersist = persist

  def run(self, state_code: str | None = None) -> None:
    """Ejecuta el ETL de un estado o de todo el catálogo geográfico."""
    if state_code is None:
      states = self._service.get_states()
      state_geometries = self._service.get_state_geometries()
      merged_states = self._merger.merge_states(states, state_geometries)
      self._persist.save_states(merged_states)
      state_codes = [item.cve_ent for item in states.datos]
    else:
      state = self._service.get_state(state_code)
      state_geometry = self._service.get_state_geometry(state_code)
      merged_state = self._merger.merge_state(state, state_geometry)
      self._persist.save_state(merged_state)
      state_codes = [state.datos.cve_ent]

    for current_state_code in state_codes:
      municipalities = self._service.get_municipalities(current_state_code)
      municipality_geometries = self._service.get_municipality_geometries(
        current_state_code
      )
      merged_municipalities = self._merger.merge_municipalities(
        municipalities, municipality_geometries
      )
      self._persist.save_municipalities(merged_municipalities)

      for municipality in municipalities.datos:
        localities = self._service.get_localities(
          current_state_code, municipality.cve_mun
        )
        locality_geometries = self._service.get_locality_geometries(
          current_state_code, municipality.cve_mun
        )
        merged_localities = self._merger.merge_localities(
          localities, locality_geometries
        )
        self._persist.save_localities(merged_localities)
