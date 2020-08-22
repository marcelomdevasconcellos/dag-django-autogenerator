from django.contrib import admin
from django.forms import Select, Textarea

from dag.models import *
from config.mixins import AuditoriaAdmin, AuditoriaAdminInline
from .functions import render_fields_obj, render_models_admins_obj


def render_fields(modeladmin, request, queryset):
    for obj in queryset:
        render_fields_obj(obj)


render_fields.short_description = "Render fields"


def update_foreignkey(modeladmin, request, queryset):
    from django.db.models import Q
    for obj in queryset:
        foreignkey = Models.objects.\
            filter(
                Q(verbose_name_plural=obj.foreignkey_txt) |
                Q(title=obj.foreignkey_txt)).all()
        if foreignkey:
            Fields.objects.filter(id=obj.id).\
                update(foreignkey=foreignkey[0])


update_foreignkey.short_description = "Update foreignkeys"


def update_field_types(modeladmin, request, queryset):
    for obj in queryset:
        type = FieldTypes.objects.filter(title=obj.field_type_txt).all()
        if type:
            Fields.objects.filter(id=obj.id).\
                update(type=type[0])


update_field_types.short_description = "Update field types"


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


class FieldsInline(AuditoriaAdminInline):
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


class ModelsInline(AuditoriaAdminInline):
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
        update_field_types,
        update_foreignkey,
    ]
    search_fields = (
        'slug',
        'verbose_name',
        'help_text',
    )
    list_filter = (
        'field_type_txt',
        'type',
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
        'type',
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


def render_models_admins(modeladmin, request, queryset):
    for obj in queryset:
        render_models_admins_obj(obj)


render_models_admins.short_description = "Render models and admins"


@admin.register(Models)
class ModelsAdmin(AuditoriaAdmin):
    actions = [
        verify_empty_tables,
        render_models_admins,
    ]
    search_fields = (
        'title',
        'verbose_name',
        'verbose_name_plural',
    )
    list_filter = (
        'django_modeladmin',
        'is_empty',
        'app',
    )
    list_display = (
        'app',
        'title',
        'verbose_name',
        'verbose_name_plural',
        'django_modeladmin',
        'is_empty',
    )
    inlines = [
        FieldsInline,
    ]
    readonly_fields = (
        'rendered_model',
        'rendered_form',
        'rendered_admin',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )


@admin.register(Apps)
class AppsAdmin(AuditoriaAdmin):
    actions = ()
    search_fields = (
        'title',
        'slug',
    )
    list_filter = (
        'is_verify',
    )
    list_display = (
        'title',
        'slug',
        'is_verify',
    )
    inlines = [
        ModelsInline,
    ]


@admin.register(FieldTypes)
class FieldTypesAdmin(AuditoriaAdmin):
    search_fields = (
        'title',
        'model_code',
    )
    list_filter = ()
    list_display = (
        'title',
        'model_code',
    )


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
