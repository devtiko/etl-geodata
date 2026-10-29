# Investigación de fuentes geográficas de INEGI

**Fecha de revisión:** 24 de octubre de 2026
**Estado:** Investigación documental con verificación puntual de rutas del Servicio Web. Las descargas directas CSV/ZIP y la cobertura exhaustiva de localidades siguen pendientes.

## 1. Objetivo y alcance

Identificar y documentar las fuentes oficiales de INEGI para consultar y descargar catálogos de entidades, municipios y localidades, así como los conjuntos vectoriales del Marco Geoestadístico.

## 2. Fuentes oficiales identificadas

| Fuente | Dirección oficial | Datos y utilidad | Estado |
|---|---|---|---|
| Catálogo Único de Claves Geoestadísticas | https://www.inegi.org.mx/app/ageeml/ | Consulta y exportación de claves y nombres de entidades, municipios y localidades; permite seleccionar filtros y fechas de corte. | Portal documentado; URL directa de CSV pendiente |
| Marco Geoestadístico | https://www.inegi.org.mx/temas/mg/ | Descarga de datos vectoriales por versión, área geográfica y capa; incluye Shapefiles. | Portal documentado; URL del ZIP estatal pendiente |
| Programa Marco Geoestadístico | https://www.inegi.org.mx/programas/mg/default.html | Información sobre versiones, capas, productos y formatos. | Portal documentado |
| Servicio Web del Catálogo Único | https://www.inegi.org.mx/servicios/catalogounico.html | Referencia oficial de consultas JSON y GeoJSON. | Rutas y cobertura verificadas puntualmente en esta investigación |
| Diccionario de datos del MG 2022 | https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463906933 | Definición de objetos, atributos y tipos de geometría de esa edición. | Referencia documental, no necesariamente aplicable a todas las versiones |

## 3. Catálogos tabulares (CSV)

El Catálogo Único registra claves y nombres de áreas geoestadísticas estatales (AGEE), municipales (AGEM) y localidades. La interfaz permite filtrar por nivel geográfico, área, fechas y opciones de exportación. Su contenido se actualiza, por lo que debe registrarse la fecha de corte del conjunto descargado.

**Información pendiente de verificar:** opciones de exportación para la entidad seleccionada, URL efectiva de descarga, encabezados, codificación, separador, formato de coordenadas, valores faltantes y cantidad de registros. No se ha comprobado una URL estática para el CSV requerido.

**Referencia:** https://www.inegi.org.mx/app/ageeml/

## 4. Archivos vectoriales (ZIP / Shapefile)

El portal del Marco Geoestadístico permite elegir versión, área geográfica y capas. La documentación describe conjuntos vectoriales en formato Shapefile, que normalmente incluyen archivos `.shp` (geometría), `.shx` (índice), `.dbf` (atributos) y `.prj` (referencia espacial). Pueden aparecer otros archivos auxiliares.

En un ZIP estatal observado previamente aparecen prefijos como `31a`, `31ar`, `31cd`, `31e`, `31ent`, `31fm`, `31l`, `31lpr`, `31m`, `31mun`, `31pe`, `31pem`, `31sia`, `31sil`, `31sip` y `31ti`. **No se ha verificado el significado de cada prefijo para la edición exacta del archivo**; no debe inferirse únicamente a partir del nombre. Consultar el diccionario de datos correspondiente a la edición descargada.

La documentación del portal menciona proyección Cónica Conforme de Lambert e ITRF2008 para ciertos productos. El sistema de referencia específico de cada conjunto se describe en su archivo `.prj` y debe comprobarse en la edición consultada.

**Pendiente:** verificar la URL directa y estabilidad del ZIP estatal de la entidad seleccionada, edición, tamaño, estructura y licencias/condiciones aplicables.

**Referencia:** https://www.inegi.org.mx/temas/mg/

## 5. Servicio web: rutas documentadas

Los siguientes patrones están publicados en la documentación oficial. Las respuestas de una selección de rutas se comprobaron en vivo; los resultados y el alcance de la comprobación se describen en esta sección.

| Consulta | URL |
|---|---|
| Catálogo de entidades, JSON | https://gaia.inegi.org.mx/wscatgeo/v2/mgee |
| Entidad, JSON | `https://gaia.inegi.org.mx/wscatgeo/v2/mgee/{cve_ent}` |
| Municipios de la entidad, JSON | `https://gaia.inegi.org.mx/wscatgeo/v2/mgem/{cve_ent}` |
| Geometrías de las entidades, GeoJSON | https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgee |
| Geometría estatal, GeoJSON | `https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgee/{cve_ent}` |
| Geometrías municipales, GeoJSON | `https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgem/{cve_ent}` |
| Localidades por municipio, JSON | `https://gaia.inegi.org.mx/wscatgeo/v2/localidades/{cve_ent}/{cve_mun}` |
| Polígonos de localidades por estado, GeoJSON | `https://gaia.inegi.org.mx/wscatgeo/v2/geo/localidades/pol/{cve_ent}` |
| Polígonos de localidades por municipio, GeoJSON | `https://gaia.inegi.org.mx/wscatgeo/v2/geo/localidades/pol/{cve_ent}/{cve_mun}` |

**Referencia:** https://www.inegi.org.mx/servicios/catalogounico.html

### Cobertura y limitaciones

- `/mgee` devolvió las 32 entidades. Las consultas `/mgem/{cve_ent}` funcionaron para las 32 claves estatales probadas y devolvieron 2,478 municipios en conjunto. `/mgem` sin clave estatal respondió HTTP 404.
- `/geo/mgee` devuelve un `FeatureCollection` GeoJSON con las geometrías de las 32 entidades.
- La consulta tabular de localidades por estado usando solo `/localidades/{cve_ent}` no funcionó en las pruebas; las rutas de localidades verificadas requieren también la clave municipal.
- Las consultas `/localidades/{cve_ent}/{cve_mun}` (JSON) y `/geo/localidades/pol/{cve_ent}/{cve_mun}` (GeoJSON) no siempre devuelven la misma cantidad de resultados; por ello, no debe suponerse correspondencia uno-a-uno entre los registros tabulares y los elementos geométricos.
- Se observaron `latitud` y `longitud` en los registros tabulares y las propiedades GeoJSON de localidades consultadas, pero no en las propiedades de geometrías municipales consultadas.
- No se recorrieron exhaustivamente todos los municipios ni todas las localidades. Estos resultados corresponden a una comprobación puntual, no a una descarga exhaustiva.

### Limitaciones por investigar

- Posibles límites de frecuencia, tamaño de respuesta, paginación y disponibilidad del servicio.
- No hay un límite numérico de peticiones por segundo confirmado en las fuentes revisadas.
- Se han observado restricciones de acceso en intentos anteriores; se debe validar el comportamiento real antes de depender de la API.
- Si se usan archivos descargables en lugar de API, verificar que las URLs sean estables y que la automatización respete las condiciones de uso.

## 6. Identificadores y campos relevantes de las APIs

Esta sección resume campos documentados u observados en las respuestas JSON y GeoJSON del Servicio Web del Catálogo Único.

**Campos JSON**

| Ruta del campo | Significado | Precaución |
|---|---|---|
| `cve_ent` | Clave estatal (dos caracteres) | Conservar ceros a la izquierda. |
| `cve_mun` | Clave municipal (tres caracteres) | Conservar como texto. |
| `cvegeo` | Clave geoestadística compuesta según nivel | Longitud variable por nivel. |
| `nomgeo` | Nombre geográfico | Revisar acentos y normalización. |
| `cve_cab` | Clave de cabecera municipal | Observada en los registros municipales consultados. |

**Campos GeoJSON**

| Ruta del campo | Significado | Precaución |
|---|---|---|
| `properties.cve_ent` | Clave estatal | Conservar ceros a la izquierda. |
| `properties.cve_mun` | Clave municipal | Conservar como texto; aplica a municipios y localidades. |
| `properties.cve_loc` | Clave de localidad | Conservar como texto; se observó en polígonos de localidades. |
| `properties.cvegeo` | Clave geoestadística compuesta según nivel | Longitud variable por nivel. |
| `properties.nomgeo` / `properties.nom_loc` | Nombre geográfico o de localidad | El nombre de la propiedad varía según la capa. |
| `properties.latitud` / `properties.longitud` | Coordenadas de referencia de localidad | Se observaron en propiedades de localidades; no sustituyen la geometría. |
| `geometry.type` | Tipo de geometría | En las respuestas consultadas se observó `MultiPolygon`. |
| `geometry.coordinates` | Coordenadas que definen la geometría espacial | Es el contenido geométrico principal; su estructura anidada depende de `type`. |

## 7. Referencias oficiales

1. INEGI, Catálogo Único: https://www.inegi.org.mx/app/ageeml/
2. INEGI, Ayuda del Catálogo Único: https://www.inegi.org.mx/contenidos/app/ageeml/Ayuda/Ayuda_Gral_Cat_Unico.pdf
3. INEGI, Marco Geoestadístico: https://www.inegi.org.mx/temas/mg/
4. INEGI, Programa Marco Geoestadístico: https://www.inegi.org.mx/programas/mg/default.html
5. INEGI, Servicio Web del Catálogo Único: https://www.inegi.org.mx/servicios/catalogounico.html
6. INEGI, Diccionario de datos del Marco Geoestadístico 2022: https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463906933

