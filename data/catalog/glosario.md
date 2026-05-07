# Glosario de negocio (ejemplo)

- **DW / destino**: base PostgreSQL configurada con variables `DEST_DB_*` en el proyecto raíz; es donde debe apuntar el Text-to-SQL en producción (solo lectura).
- **Origen / topus**: base operativa (`ORIGIN_DB_*` o `topusDB`); no usar para analítica salvo que el catálogo lo autorice explícitamente.
- **ETL**: pipelines en `utilizacion/`, `tiempos_carga/`, `movimientos_contenedores/` y `dw/` que poblan el destino.

- **Tipo de servicio / tipos de servicios** (negocio TNM, IMPO/EXPO/importación/exportación): columna
  `public.caracteristicas.impo_expo`, cruce `fact_servicios.fk_caracteristicas = caracteristicas.id_caracteristicas`.
  No confundir con **tipo de etapa** (`public.etapa.codigo` = almacenaje, retiro, presentación, devolución).

Añade aquí sinónimos ("programación", "viaje", "servicio") mapeados a tablas/columnas concretas cuando las tengas definidas.
