SELECT m.id, m.title, m.verbose_name, m.verbose_name_plural, m.django_modeladmin, 
m.rendered_model, m.rendered_form, m.rendered_admin, m.app_id, a.slug, m.is_empty
	FROM public.dag_models m 
	JOIN public.dag_apps a ON a.id = m.app_id;



	SELECT f.id, f.slug, f.help_text, f.max_length, f.default_value, 
f.is_null, f.is_blank, f.is_unique, f.is_readonly, f.is_editable, 
f.is_db_index, f.is_ordering, f."order", f.is_model_title, 
f.in_search_fields, f.in_list_filter, f.in_list_display, 
f.in_field_model, 
--f.rendered_model_django, f.rendered_form_django, 
--f.rendered_table_html, f.rendered_form_html, 
--f.rendered_filter_html, f.rendered_filter_dict, 
f.foreignkey_id, f.model_id, 
f.choices, f.verbose_name, f.fieldtype_id, fieldtype_title, f.foreignkey_model_title,
m.title AS model_title
	FROM public.dag_fields f
	LEFT JOIN public.dag_models m ON f.model_id = m.id
	LEFT JOIN public.dag_models mfk ON f.foreignkey_id = mfk.id
	LEFT JOIN public.dag_fieldtypes t ON f.fieldtype_id = t.id;