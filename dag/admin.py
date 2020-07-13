from django.contrib import admin
from django.forms import Select, Textarea

from dag.models import *
from dag_django_autogenerate.mixins import AuditoriaAdmin, AuditoriaAdminInline




@admin.register(Fields)
class FieldsAdmin(AuditoriaAdmin):
    search_fields = (
        'title',
        'verbose_name',
        'verbose_name_plural',
        'title',
        'slug',
        'help_text',
    )
    list_filter = (
        'model',
        'field_type',
        'foreignkey',
        'choice',
        'max_length',
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
        'field_type',
        'foreignkey',
        'choice',
        'title',
        'slug',
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
    )


class FieldsInline(AuditoriaAdminInline):
    model = Fields
    fk_name = 'model'
    extra = 4
    list_display = (
        'field_type',
        'title',
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


@admin.register(Models)
class ModelsAdmin(AuditoriaAdmin):
    search_fields = (
        'title',
        'verbose_name',
        'verbose_name_plural',
    )
    list_filter = (
        'inline_models',
        'django_modeladmin',
    )
    list_display = (
        'app',
        'title',
        'verbose_name',
        'verbose_name_plural',
        'django_modeladmin',
    )
    inlines = [
        FieldsInline,
    ]


class ModelsInline(AuditoriaAdminInline):
    model = Models
    extra = 4
    list_display = (
        'title',
        'verbose_name',
        'verbose_name_plural',
        'django_modeladmin',
    )


@admin.register(Apps)
class AppsAdmin(AuditoriaAdmin):
    search_fields = ('title', 'slug')
    list_filter = ()
    list_display = ('title', 'slug')
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


class ChoicesValuesInline(AuditoriaAdminInline):
    model = ChoicesValues
    extra = 1
    list_display = (
        'key',
        'value',
    )
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={
                'rows': 4,
                'cols': 40
            })
        },
        models.ForeignKey: {
            'widget': Select(attrs={
                'style': 'width:150px'
            })
        },
    }


@admin.register(ChoicesValues)
class ChoicesValuesAdmin(AuditoriaAdmin):
    search_fields = (
        'key',
        'value',
    )
    list_filter = (
        'choice',
    )
    list_display = (
        'choice',
        'key',
        'value',
    )


@admin.register(Choices)
class ChoicesAdmin(AuditoriaAdmin):
    search_fields = (
        'title',
    )
    list_filter = ()
    list_display = (
        'title',
    )
    inlines = [
        ChoicesValuesInline,
    ]


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
