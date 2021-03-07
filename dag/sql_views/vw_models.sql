DROP VIEW IF EXISTS vw_models;
CREATE OR REPLACE VIEW vw_models AS
 
WITH temp AS (
SELECT DISTINCT 
	   e.app AS app,
       unnest(string_to_array(e.model, ', ')) AS model,
	   MIN(e.id) AS id_esocial, 
	   NULL::int AS id_legado
  FROM public.esocial_leiaute e
 GROUP BY e.app, unnest(string_to_array(e.model, ', '))
 UNION
SELECT DISTINCT 
	   l.app AS app, 
       l.table_name_new AS model, 
	   NULL::int AS id_esocial, 
	   MIN(l.id) AS id_legado
  FROM public.legado_tabelas l
 GROUP BY l.app, l.table_name_new) 
 
SELECT DISTINCT 
       0 AS id,
       app,
	   model,
	   CASE
	   WHEN SUM(id_esocial) > 0 THEN True
	   ELSE False 
	   END AS esocial,
	   CASE
	   WHEN SUM(id_legado) > 0 THEN True
	   ELSE False 
	   END AS legado
  FROM temp 
 GROUP BY app, model
 ORDER BY app, model;