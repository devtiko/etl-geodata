# etl-geodata

ETL que consulta el Servicio Web del Catálogo Único de INEGI, combina los datos geográficos con sus geometrías y los guarda localmente en JSON y GeoJSON. Puede procesar una entidad federativa o todo el catálogo.

## Requisitos

- Python 3.12 o posterior
- [uv](https://docs.astral.sh/uv/)

## Instalación

Desde la raíz del proyecto, instala las dependencias:

```bash
uv sync
```

## Uso

Procesar todas las entidades:

```bash
uv run etl
```

Procesar una entidad por su clave INEGI (de `1` a `32`; se aceptan claves con o sin cero inicial):

```bash
uv run etl --state 31
```

Por defecto se reutiliza la caché de solicitudes. Para forzar una nueva consulta al servicio:

```bash
uv run etl --state 31 --refresh
```

Los archivos obtenidos se guardan bajo `data/`, organizados en datos originales (`data/raw/`) y resultados geográficos combinados. La ejecución sin `--state` procesa las 32 entidades y sus municipios y localidades, por lo que puede realizar muchas solicitudes.

Para más información sobre las fuentes y las rutas consultadas, consulta [`docs/research.md`](docs/research.md).

## Limitaciones

- El tiempo de ejecución depende de la cantidad de datos solicitados y de la disponibilidad del servicio de INEGI.
- Procesar todas las entidades implica solicitudes para sus municipios y localidades, por lo que puede tardar y requiere una conexión a internet estable.
- La caché se reutiliza por defecto; usa `--refresh` para consultar nuevamente el servicio.
