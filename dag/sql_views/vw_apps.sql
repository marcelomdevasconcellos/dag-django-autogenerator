DROP VIEW IF EXISTS vw_apps;
CREATE OR REPLACE VIEW vw_apps AS
 
 WITH temp AS (
SELECT DISTINCT 
	   e.app AS app, 
	   MIN(e.id) AS id_esocial, 
	   NULL::int AS id_legado
  FROM public.esocial_leiaute e
 GROUP BY e.app
 UNION
SELECT DISTINCT 
	   l.app AS legado_app, 
	   NULL::int AS id_esocial, 
	   MIN(l.id) AS id_legado
  FROM public.legado_tabelas l
 GROUP BY l.app) 
 
SELECT DISTINCT
       0 AS id,
       app,
	   CASE
	   WHEN SUM(id_esocial) > 0 THEN True
	   ELSE False 
	   END AS esocial,
	   CASE
	   WHEN SUM(id_legado) > 0 THEN True
	   ELSE False 
	   END AS legado
  FROM temp 
 GROUP BY app
 ORDER BY app;