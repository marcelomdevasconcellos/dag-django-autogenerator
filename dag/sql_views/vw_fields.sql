DROP VIEW IF EXISTS vw_fields;
CREATE OR REPLACE VIEW vw_fields AS
 
WITH temp AS (
SELECT DISTINCT
	   e.app AS app, 
       unnest(string_to_array(e.model, ', ')) AS model,
	   e.field AS field,
	   MIN(e.id) AS id_esocial, 
	   NULL::int AS id_legado
  FROM public.esocial_leiaute e
 GROUP BY e.app, e.model, e.field
 UNION
SELECT DISTINCT
	   t.app AS app,
       t.table_name_new AS model,
	   l.column_name_new AS field,
	   NULL::int AS id_esocial,
	   MIN(l.id) AS id_legado
  FROM public.legado_campos l
 JOIN public.legado_tabelas t ON t.table_name = l.table_name
 GROUP BY t.app, t.table_name_new, l.column_name_new)
 
SELECT DISTINCT
       ROW_NUMBER() OVER (ORDER BY app, model, field) AS id,
       app,
	   model,
	   field,
	   CASE
	   WHEN SUM(id_esocial) > 0 THEN True
	   ELSE False 
	   END AS esocial,
	   CASE
	   WHEN SUM(id_legado) > 0 THEN True
	   ELSE False 
	   END AS legado
  FROM temp 
 GROUP BY app, model, field
 ORDER BY app, model, field;