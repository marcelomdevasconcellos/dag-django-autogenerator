from django.contrib import admin

from config.mixins import AuditoriaAdmin, AuditoriaAdminTabularInline
from dag.models import BusinessRulesCode, BusinessRules, Models, Apps, Fields, ModelFunctions, CustomModels, Variables


def render_fields(modeladmin, request, queryset):
    from django.template import Template, Context
    for obj in queryset:
        context = {
            'f': obj,
        }
        template = '{% load templatetags %}{% autoescape off %}' + \
            obj.type.model_code + '{% endautoescape %}'
        t = Template(template)
        context = Context(context)
        rendered_model_django = t.render(context)
        Fields.objects.\
            filter(id=obj.id).\
            update(rendered_model_django=rendered_model_django)


render_fields.short_description = "Render fields"


def update_foreignkey(modeladmin, request, queryset):
    for obj in queryset:
        foreignkey = Models.objects.filter(title=obj.foreignkey_txt).all()
        if foreignkey:
            Fields.objects.filter(id=obj.id).update(foreignkey=foreignkey[0])


update_foreignkey.short_description = "Update foreignkeys"


def verify_empty_tables(modeladmin, request, queryset):
    for obj in queryset:
        q = Fields.objects.filter(model=obj).all()
        if q:
            Models.objects.\
                filter(id=obj.id).\
                update(is_empty=False)
        else:
            Models.objects.\
                filter(id=obj.id).\
                update(is_empty=True)


verify_empty_tables.short_description = "Verify empty tables"


class FieldsInline(AuditoriaAdminTabularInline):
    model = Fields
    fk_name = 'model'
    extra = 4
    list_display = (
        'title',
        'slug',
        'help_text',
        'field_type_txt',
        'foreignkey',
        'max_length',
        'default_value',
        'is_null',
        'is_blank',
        'is_unique',
        'is_readonly',
        'is_editable',
        'is_db_index',
        'is_ordering',
        'is_model_title',
        'in_search_fields',
        'in_list_filter',
        'in_list_display',
        'in_field_model',
        'order',
    )
    readonly_fields = (
        'rendered_model_django',
        'rendered_form_django',
        'rendered_table_html',
        'rendered_form_html',
        'rendered_filter_html',
        'rendered_filter_dict',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )


class ModelsInline(AuditoriaAdminTabularInline):
    model = Models
    extra = 4
    list_display = (
        'title',
        'verbose_name',
        'verbose_name_plural',
        'django_modeladmin',
        'count_rows',
    )


@admin.register(Fields)
class FieldsAdmin(AuditoriaAdmin):
    actions = [
        render_fields,
        update_foreignkey,
    ]
    search_fields = (
        'slug',
        'verbose_name',
        'help_text',
    )
    list_filter = (
        'field_type_txt',
        'foreignkey_txt',
        'foreignkey',
        'model',
        'is_null',
        'is_blank',
        'is_unique',
        'is_readonly',
        'is_editable',
        'is_db_index',
        'is_ordering',
        'is_model_title',
        'in_search_fields',
        'in_list_filter',
        'in_list_display',
        'in_field_model',
    )
    list_display = (
        'model',
        'slug',
        'verbose_name',
        'field_type_txt',
        'foreignkey',
        'max_length',
        'default_value',
        'is_null',
        'is_blank',
        'is_unique',
        'is_readonly',
        'is_editable',
        'is_db_index',
        'is_ordering',
        'order',
        'is_model_title',
        'in_search_fields',
        'in_list_filter',
        'in_list_display',
        'in_field_model',
    )
    readonly_fields = (
        'model_title',
        'fieldtype_title',
        'foreignkey_model_title',
        'rendered_model_django',
        'rendered_form_django',
        'rendered_table_html',
        'rendered_form_html',
        'rendered_filter_html',
        'rendered_filter_dict',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )


@admin.register(Models)
class ModelsAdmin(AuditoriaAdmin):
    actions = [
        verify_empty_tables,
    ]
    search_fields = (
        'title',
        'verbose_name',
        'verbose_name_plural',
    )
    list_filter = (
        'is_empty',
        'is_model_admin',
        'is_read_only',
        'app',
    )
    list_display = (
        'app',
        'title',
        'verbose_name',
        'verbose_name_plural',
        'is_model_admin',
        'is_read_only',
        'is_empty',
    )
    inlines = [
        FieldsInline,
    ]


@admin.register(Apps)
class AppsAdmin(AuditoriaAdmin):
    search_fields = ('title', 'slug')
    list_filter = ()
    list_display = ('title', 'slug')
    inlines = [
        ModelsInline,
    ]


@admin.register(CustomModels)
class CustomModelsAdmin(AuditoriaAdmin):
    search_fields = (
        'title',
        'slug',
    )
    list_filter = (
        'app',
    )
    list_display = (
        'app',
        'title',
        'slug',
    )


@admin.register(ModelFunctions)
class ModelFunctionsAdmin(AuditoriaAdmin):
    search_fields = (
        'title',
        'slug',
    )
    list_filter = (
        'model',
    )
    list_display = (
        'model',
        'title',
        'slug',
    )


@admin.register(Variables)
class VariablesAdmin(AuditoriaAdmin):
    search_fields = (
        'title',
        'key',
        'code',
    )
    list_filter = ()
    list_display = (
        'title',
        'key',
        'code',
    )


class BusinessRulesCodeInline(AuditoriaAdminTabularInline):
    model = BusinessRulesCode
    extra = 4
    list_display = (
        'title',
        'func',
        'code',
    )


@admin.register(BusinessRules)
class BusinessRulesAdmin(AuditoriaAdmin):
    search_fields = (
        'title',
        'description',
    )
    list_filter = (
        'app_title',
        'model_title',
        'model')
    list_display = (
        'title',
        'description',
        'app_title',
        'model_title',
        'model'
    )
