# Glosario de negocio TNM

- **DW / destino**: base PostgreSQL configurada con variables `DEST_DB_*` en el proyecto raíz; es donde debe apuntar el Text-to-SQL en producción (solo lectura).
- **Origen / topus**: base operativa (`ORIGIN_DB_*` o `topusDB`); no usar para analítica salvo que el catálogo lo autorice explícitamente.
- **ETL**: pipelines en `utilizacion/`, `tiempos_carga/`, `movimientos_contenedores/` y `dw/` que poblan el destino.

## Tipo de servicio comercial (`public.caracteristicas.impo_expo`)

Una "tipo de servicio" en negocio TNM se almacena en la columna **`impo_expo`** de
`public.caracteristicas`, que se une al hecho con el JOIN canónico
`caracteristicas.id_caracteristicas = fact_servicios.id`. **No** confundir con `etapa.codigo` (tipo
de etapa operativa).

Mapeo término de negocio → valor exacto en `caracteristicas.impo_expo`:

| Término(s) en lenguaje natural | Valor en `impo_expo` |
|---|---|
| importación, importacion, IMPO, import | `IMPO` |
| exportación, exportacion, EXPO, export | `EXPO` |
| desconsolidado, desconsolidación, desconsolidacion, DESC | `DESC` |
| depósito, deposito, DEPO | `DEPO` |
| almacenaje (en sentido comercial, **no** la etapa), ALM | `ALM` |
| flete, FLETE | `FLETE` |
| portuario, port, PORT | `PORT` |
| stacking, stack, STACK | `STACK` |

Patrón de filtro: `WHERE TRIM(c.impo_expo) = 'DESC'` (igual para los demás códigos).
Para agrupar: `GROUP BY TRIM(c.impo_expo)`.

## Tipo de etapa (`public.etapa.codigo`)

Etapa operativa del flujo del servicio (almacenaje físico, retiro, presentación documental,
devolución del contenedor). Nada que ver con `impo_expo`.

| Código | Significado |
|---|---|
| `'0'` | Almacenaje |
| `'1'` | Retiro |
| `'2'` | Presentación |
| `'3'` | Devolución |

Filtrar como **texto**: `WHERE e.codigo = '1'`.

## Identificadores y formato de literales

### Número de contenedor
Vive en **`public.caracteristicas.numero_contenedor`** (`varchar`). Formato estándar
ISO 6346 reducido en TNM: **`AAAANNNNNN-N`** (4 letras + 6 dígitos + guion + 1 dígito de
control), por ejemplo `TCNU431549-1`. Reglas:

- **Siempre se compara como texto entre comillas simples**: `... = 'TCNU431549-1'`.
- **Normalizar a mayúsculas y sin espacios** antes de comparar:
  `TRIM(UPPER(c.numero_contenedor)) = 'TCNU431549-1'`.
- Si el usuario escribe el código en minúsculas (`tcnu431549-1`) o con espacios,
  igualmente se debe pasar a mayúsculas en el literal.
- **Hay otra columna `numero_contenedor` en `public.stock`** (módulo de almacenaje), pero
  el contenedor del servicio canónico vive en `caracteristicas`. Para preguntas de servicio
  (retiro, presentación, devolución, IMPO/EXPO, etc.) usa `caracteristicas`.

### RUT (cliente, comercial, conductor)
Texto entre comillas simples: `cf.rut = '76123456-K'`. Normalizar mayúsculas y sin puntos:
`UPPER(REPLACE(REPLACE(cf.rut, '.', ''), ' ', '')) = '76123456-K'`.

### ID de servicio (`fk_servicio`)
Es **integer**, va sin comillas: `fs.fk_servicio = 153342`. Si el usuario dice
«servicio 153342» o «id 153342» se filtra por `fs.fk_servicio` (no por `fs.id`,
que es el surrogate del DW).

## Sinónimos comunes

- **Servicio / viaje** (en negocio): identificador operativo `fk_servicio` en
  dimensiones; `COUNT(DISTINCT fs.fk_servicio)` cuenta servicios distintos.
- **Contenedor**: número alfanumérico `caracteristicas.numero_contenedor`
  (ver sección de identificadores arriba). Un servicio puede tener un contenedor asociado.
- **Programación / fecha programada / fecha de etapa 1**: `public."time".etapa_1_fecha`.
- **Cliente** (sin más): `public.cliente_facturacion` (PK `id_customer`, columnas `name`, `rut`).
- **Cliente despacho** o **consignatario**: `public.cliente_despacho`.
- **Comercial / ejecutivo**: `public.comercial`.
- **Conductor / chofer**: `public.conductor`.
- **Nave / barco / vessel**: `public.nave`.
