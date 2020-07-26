from django.contrib import admin
from django.forms import Select, Textarea

from dag.models import *
from config.mixins import AuditoriaAdmin, AuditoriaAdminInline


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
        'field_type',
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
    search_fields = (
        'title',
        'verbose_name',
        'help_text',
    )
    list_filter = (
        'model',
        'field_type',
        'foreignkey',
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
        'is_check',
    )
    list_display = (
        'model',
        'title',
        'verbose_name',
        'field_type',
        'foreignkey',
        'help_text',
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
        'is_check',
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
        'django_modeladmin',
        'is_empty',
        'is_check',
    )
    list_display = (
        'app',
        'title',
        'verbose_name',
        'verbose_name_plural',
        'django_modeladmin',
        'is_empty',
        'is_check',
    )
    inlines = [
        FieldsInline,
    ]


@admin.register(Apps)
class AppsAdmin(AuditoriaAdmin):
    search_fields = ('title', 'slug')
    list_filter = (
        'is_check',
    )
    list_display = (
        'title',
        'slug',
        'is_check',
    )
    inlines = [
        ModelsInline,
    ]


@admin.register(FieldTypes)
class FieldTypesAdmin(AuditoriaAdmin):
    search_fields = (
        'title',
        'model_code',
        'is_check',
    )
    list_filter = ()
    list_display = (
        'title',
        'model_code',
        'is_check',
    )


@admin.register(CustomModels)
class CustomModelsAdmin(AuditoriaAdmin):
    search_fields = (
        'title',
        'slug',
    )
    list_filter = (
        'app',
        'is_check',
    )
    list_display = (
        'app',
        'title',
        'slug',
        'is_check',
    )


@admin.register(ModelFunctions)
class ModelFunctionsAdmin(AuditoriaAdmin):
    search_fields = (
        'title',
        'slug',
    )
    list_filter = (
        'model',
        'is_check',
    )
    list_display = (
        'model',
        'title',
        'slug',
        'is_check',
    )


@admin.register(Variables)
class VariablesAdmin(AuditoriaAdmin):
    search_fields = (
        'title',
        'key',
        'code',
    )
    list_filter = (
        'is_check',
    )
    list_display = (
        'title',
        'key',
        'code',
        'is_check',
    )
